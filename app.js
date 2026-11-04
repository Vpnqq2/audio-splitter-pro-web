"use strict";
/* AudioSplitAI (web): pick a song, choose the tracks, split with the AI model (worker.js), mix, export WAV. */
const SR = 44100;
// UI order: vocals, drums, bass, other. `stem` is the index of that track in the model output (drums, bass, other, vocals).
const CH = [
  { key: "vocals", label: "Vocals", stem: 3, color: "#00C78A", icon: "🎤", hint: "Singing and voices" },
  { key: "drums",  label: "Drums",  stem: 0, color: "#2BB5FF", icon: "🥁", hint: "Beats and percussion" },
  { key: "bass",   label: "Bass",   stem: 1, color: "#FF9F1C", icon: "🎸", hint: "The bass line" },
  { key: "other",  label: "Other",  stem: 2, color: "#C04CFF", icon: "🎹", hint: "Guitar, keys and the rest" },
];
const $ = (s, r = document) => r.querySelector(s);
const fmt = (s) => { s = Math.max(0, Math.round(s)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); };

const S = {
  file: null, name: "", left: null, right: null, seconds: 0,
  picks: [true, true, true, true],
  worker: null,
  mix: null,            // mixer engine once a split is done
  rafId: 0,
};

// ---------------------------------------------------------------- screens & small helpers
function show(id) {
  const first = !S.screen;
  document.querySelectorAll(".screen").forEach((el) => { el.hidden = el.id !== "s-" + id; });
  S.screen = id;
  if (!first) {   // keep the tool in view when the screen changes
    const box = $("#tool-box"), top = box.getBoundingClientRect().top;
    if (top < 60 || top > innerHeight * 0.5) box.scrollIntoView({ block: "start" });
  }
}
let toastTimer = 0;
function toast(msg) {
  const t = $("#toast"); t.textContent = msg; t.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, 3800);
}
const baseName = () => (S.name || "song").replace(/\.[^.]+$/, "").replace(/[^\p{L}\p{N}_ -]/gu, "_");

// ---------------------------------------------------------------- home
(function initHome() {
  const heights = [.16, .30, .22, .42, .58, .80, 1, .72, .52, .36, .30, .20, .12];
  const w = $("#hero-wave");
  heights.forEach((h, i) => {
    const b = document.createElement("i");
    b.style.setProperty("--h", Math.round(h * 84) + "px"); b.style.setProperty("--d", (i * -0.18).toFixed(2) + "s");
    b.style.background = i < 5 ? "#00A875" : "#00C78A";
    w.appendChild(b);
  });
  $("#file").addEventListener("change", (e) => { const f = e.target.files[0]; e.target.value = ""; if (f) loadFile(f); });
  const app = document.body, dz = $("#dropzone");
  ["dragover", "dragenter"].forEach((ev) => app.addEventListener(ev, (e) => { e.preventDefault(); if (S.screen === "home") dz.classList.add("drag"); }));
  ["dragleave", "dragend"].forEach((ev) => app.addEventListener(ev, (e) => { if (!e.relatedTarget) dz.classList.remove("drag"); }));
  app.addEventListener("drop", (e) => {
    e.preventDefault(); dz.classList.remove("drag");
    if (S.screen !== "home") return;
    const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) loadFile(f);
  });
  if (!window.crossOriginIsolated && window.isSecureContext && "serviceWorker" in navigator) $("#iso-note").hidden = false;
  if (navigator.gpu) $("#gpu-row").hidden = false;
})();

// ---------------------------------------------------------------- loading a file
async function loadFile(file) {
  S.file = file; S.name = file.name; S.left = S.right = null;
  S.picks = [true, true, true, true];
  show("pick");
  $("#pick-name").textContent = file.name;
  $("#pick-info").textContent = "Reading file...";
  $("#split").disabled = true; $("#pick-warn").hidden = true;
  renderTiles();
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: SR });
    const buf = await ctx.decodeAudioData(await file.arrayBuffer());
    ctx.close();
    S.left = buf.getChannelData(0).slice();
    S.right = buf.numberOfChannels > 1 ? buf.getChannelData(1).slice() : S.left.slice();
    S.seconds = buf.duration;
    $("#pick-info").textContent = fmt(buf.duration) + " • " + (file.size / 1e6).toFixed(1) + " MB";
    if (buf.duration > 480) {
      const w = $("#pick-warn"); w.hidden = false;
      w.textContent = "This song is long (" + fmt(buf.duration) + "). The browser needs a lot of memory for it; if the page crashes, try a shorter song.";
    }
    $("#split").disabled = false;
  } catch (err) {
    $("#pick-info").textContent = "This file could not be read. Try an MP3, M4A, WAV or FLAC file.";
  }
}

// ---------------------------------------------------------------- choosing tracks
function renderTiles() {
  const box = $("#tiles"); box.innerHTML = "";
  CH.forEach((c, i) => {
    const b = document.createElement("button");
    b.className = "tile" + (S.picks[i] ? " on" : ""); b.style.setProperty("--c", c.color);
    b.innerHTML = '<span class="ck">✓</span><span class="ic">' + c.icon + "</span><b>" + c.label + "</b><span>" + c.hint + "</span>";
    b.onclick = () => { if (S.picks[i] && S.picks.filter(Boolean).length === 1) return; S.picks[i] = !S.picks[i]; renderTiles(); };
    box.appendChild(b);
  });
  const n = S.picks.filter(Boolean).length;
  $("#split").textContent = n === 4 ? "Split all 4 tracks" : n === 1 ? "Split " + CH[S.picks.indexOf(true)].label + " only" : "Split " + n + " tracks";
  const set = n === 4 ? "all" : (n === 1 && S.picks[0]) ? "vocals" : (n === 3 && !S.picks[0]) ? "novocals" : "";
  document.querySelectorAll(".chip").forEach((c) => c.classList.toggle("on", c.dataset.set === set));
}
document.querySelectorAll(".chip").forEach((c) => c.addEventListener("click", () => {
  const s = c.dataset.set;
  S.picks = s === "all" ? [true, true, true, true] : s === "vocals" ? [true, false, false, false] : [false, true, true, true];
  renderTiles();
}));
$("#pick-back").onclick = () => show("home");

// ---------------------------------------------------------------- splitting
function setRing(p) {
  $("#ring-arc").style.strokeDashoffset = String(326.7 * (1 - p));
  $("#proc-pct").textContent = Math.round(p * 100) + "%";
}
function stopWorker() { if (S.worker) { S.worker.terminate(); S.worker = null; } releaseAwake(); }
// keep the screen on while splitting: a sleeping phone slows the page down a lot
let wake = null;
async function keepAwake() { try { if (navigator.wakeLock && !wake) { wake = await navigator.wakeLock.request("screen"); wake.addEventListener("release", () => { wake = null; }); } } catch (_) {} }
function releaseAwake() { try { if (wake) wake.release(); } catch (_) {} wake = null; }
document.addEventListener("visibilitychange", () => { if (!document.hidden && S.worker) keepAwake(); });

// level 0 = normal, 1 = lighter (2 threads), 2 = lightest (1 thread). Each level uses less memory than the one before.
function startSplit(level) {
  level = typeof level === "number" ? level : 0;
  const safe = level > 0;
  if (!S.left) return;
  const stems = CH.filter((_, i) => S.picks[i]).map((c) => c.stem);
  const div = Number($("#quality").value);
  const gpu = !$("#gpu-row").hidden && $("#gpu").checked;
  const threads = window.crossOriginIsolated ? Math.min(level === 0 ? 4 : level === 1 ? 2 : 1, navigator.hardwareConcurrency || 4) : 1;
  show("proc"); setRing(0);
  $("#proc-title").textContent = safe ? "Trying a lighter mode (" + level + "/2)..." : "Preparing..."; $("#proc-status").textContent = "Starting..."; $("#proc-eta").textContent = "";
  $("#dl-wrap").hidden = true;
  stopWorker();
  const left = S.left.slice(), right = S.right.slice();   // copies go to the worker; the originals stay for a retry
  const picks = S.picks.slice();
  const w = new Worker("worker.js"); S.worker = w;
  w.onerror = (e) => { if (level < 2) { stopWorker(); startSplit(level + 1); } else fail("The AI engine could not start: " + (e.message || "unknown error")); };
  w.onmessage = (e) => {
    const m = e.data;
    if (m.type === "status") $("#proc-status").textContent = m.text;
    else if (m.type === "download") {
      $("#dl-wrap").hidden = false; $("#dl-fill").style.width = Math.round(m.p * 100) + "%"; setRing(m.p);
      $("#proc-title").textContent = "Downloading the AI engine";
    } else if (m.type === "ready") {
      $("#dl-wrap").hidden = true;
      $("#proc-title").textContent = "Processing your audio..."; $("#proc-status").textContent = m.gpu ? "Using the graphics card"
        : "Separating the tracks (" + m.threads + (m.threads === 1 ? " thread" : " threads") + (m.isolated ? "" : ", reload the page once to use more") + (m.safe ? ", light mode" : "") + ")";
      keepAwake();
      setRing(0);
      w.postMessage({ type: "run", left, right, stems, div }, [left.buffer, right.buffer]);
    } else if (m.type === "progress") {
      setRing(m.p);
      $("#proc-eta").textContent = m.eta > 0 ? "About " + Math.max(1, Math.round(m.eta / 60)) + " min left" : "";
    } else if (m.type === "done") {
      stopWorker(); S.left = S.right = null; buildMixer(m.stems, picks);
    } else if (m.type === "error") {
      if (m.retry && level < 2) { stopWorker(); startSplit(level + 1); return; }   // out of memory etc.: try the light mode once
      fail(m.retry ? "Your browser ran out of memory for the AI engine (" + m.message + "). Try a computer, Chrome, or a shorter song." : m.message);
    }
  };
  w.postMessage({ type: "init", gpu: gpu && !safe, threads, safe });
}
function fail(msg) {
  stopWorker(); show("home"); toast(msg);
}
$("#split").onclick = startSplit;
$("#cancel").onclick = () => { stopWorker(); show("home"); };

// ---------------------------------------------------------------- mixer
class Mixer {
  constructor(items) {            // items: [{ idx (UI index), buffer (AudioBuffer) }]
    this.ctx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: SR });
    this.master = this.ctx.createGain(); this.master.connect(this.ctx.destination);
    this.chs = items.map((it) => {
      const gain = this.ctx.createGain(), an = this.ctx.createAnalyser(); an.fftSize = 512;
      gain.connect(an); an.connect(this.master);
      return { idx: it.idx, buffer: it.buffer, gain, an, vol: 0.7, mute: false, solo: false, src: null, peaks: peaksOf(it.buffer, 200), data: new Float32Array(512) };
    });
    this.duration = items[0].buffer.duration;
    this.playing = false; this.offset = 0; this.startedAt = 0; this.loop = false; this.gen = 0;
    this.apply();
  }
  pos() { return this.playing ? Math.min(this.duration, this.ctx.currentTime - this.startedAt) : this.offset; }
  apply() {
    const anySolo = this.chs.some((c) => c.solo);
    for (const c of this.chs) {
      const audible = anySolo ? c.solo : !c.mute;
      c.audible = audible;
      c.gain.gain.setTargetAtTime(audible ? c.vol / 0.7 : 0, this.ctx.currentTime, 0.015);   // 70% = the original level
    }
  }
  play() {
    if (this.playing) return;
    this.ctx.resume();
    if (this.offset >= this.duration - 0.05) this.offset = 0;
    const gen = ++this.gen;
    for (const c of this.chs) {
      const s = this.ctx.createBufferSource(); s.buffer = c.buffer; s.loop = this.loop; s.connect(c.gain);
      s.start(0, this.offset); c.src = s;
    }
    this.startedAt = this.ctx.currentTime - this.offset; this.playing = true;
    const first = this.chs[0].src;
    first.onended = () => { if (gen === this.gen && !this.loop) { this.playing = false; this.offset = 0; updatePlayBtn(); } };
  }
  stopSources() { this.gen++; for (const c of this.chs) { if (c.src) { try { c.src.onended = null; c.src.stop(); } catch (_) {} c.src = null; } } }
  pause() { if (!this.playing) return; this.offset = this.pos(); this.stopSources(); this.playing = false; }
  seek(t) { const was = this.playing; if (was) this.stopSources(); this.playing = false; this.offset = Math.max(0, Math.min(this.duration, t)); if (was) this.play(); }
  setLoop(v) { this.loop = v; for (const c of this.chs) if (c.src) c.src.loop = v; }
  close() { this.stopSources(); this.ctx.close(); }
  get karaokeAvailable() { return this.chs.some((c) => c.idx === 0) && this.chs.length > 1; }
  get karaokeOn() { const v = this.chs.find((c) => c.idx === 0); return this.karaokeAvailable && v.mute && !this.chs.some((c) => c.solo) && this.chs.filter((c) => c !== v).every((c) => !c.mute); }
  toggleKaraoke() {
    if (!this.karaokeAvailable) return;
    const v = this.chs.find((c) => c.idx === 0);
    if (this.karaokeOn) v.mute = false;
    else for (const c of this.chs) { c.solo = false; c.mute = c === v; }
    this.apply();
  }
}
function peaksOf(buf, bins) {
  const a = buf.getChannelData(0), b = buf.numberOfChannels > 1 ? buf.getChannelData(1) : a, out = new Float32Array(bins);
  const step = a.length / bins; let mx = 0.001;
  for (let i = 0; i < bins; i++) {
    let p = 0; const s0 = Math.floor(i * step), s1 = Math.floor((i + 1) * step);
    for (let j = s0; j < s1; j += 12) { const v = Math.max(Math.abs(a[j]), Math.abs(b[j])); if (v > p) p = v; }
    out[i] = p; if (p > mx) mx = p;
  }
  for (let i = 0; i < bins; i++) out[i] /= mx;
  return out;
}

function buildMixer(stemResults, picks) {
  const probe = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: SR });
  const items = [];
  CH.forEach((c, idx) => {
    if (!picks[idx]) return;
    const r = stemResults.find((x) => x.stem === c.stem);
    const n = r.left.length, buf = probe.createBuffer(2, n, SR);
    const L = buf.getChannelData(0), R = buf.getChannelData(1);
    for (let i = 0; i < n; i++) { L[i] = r.left[i] / 32768; R[i] = r.right[i] / 32768; }
    items.push({ idx, buffer: buf });
  });
  probe.close();
  if (S.mix) S.mix.close();
  S.mix = new Mixer(items);
  $("#mix-name").textContent = S.name;
  $("#t-dur").textContent = fmt(S.mix.duration);
  $("#karaoke").hidden = !S.mix.karaokeAvailable;
  const box = $("#strips"); box.innerHTML = "";
  S.mix.chs.forEach((c) => {
    const ch = CH[c.idx];
    const el = document.createElement("div"); el.className = "strip"; el.style.setProperty("--c", ch.color);
    el.innerHTML = '<div class="top"><span class="ic">' + ch.icon + '</span><span class="nm">' + ch.label + '</span><span class="st">ON</span></div>' +
      '<canvas></canvas><div class="meter"><i></i></div>' +
      '<div class="ctl"><input type="range" min="0" max="100" value="70" aria-label="' + ch.label + ' volume"><span class="vol">70%</span>' +
      '<button class="tg s" aria-label="Solo ' + ch.label + '">S</button><button class="tg m" aria-label="Mute ' + ch.label + '">M</button></div>';
    c.el = el; c.canvas = el.querySelector("canvas"); c.meterEl = el.querySelector(".meter i");
    c.stEl = el.querySelector(".st"); c.volEl = el.querySelector(".vol");
    el.querySelector('input[type=range]').oninput = (e) => { c.vol = e.target.value / 100; c.volEl.textContent = e.target.value + "%"; S.mix.apply(); refreshStrips(); };
    el.querySelector(".s").onclick = () => { c.solo = !c.solo; S.mix.apply(); refreshStrips(); };
    el.querySelector(".m").onclick = () => { c.mute = !c.mute; S.mix.apply(); refreshStrips(); };
    c.canvas.onclick = (e) => { const r = c.canvas.getBoundingClientRect(); S.mix.seek((e.clientX - r.left) / r.width * S.mix.duration); };
    box.appendChild(el);
  });
  refreshStrips(); updatePlayBtn();
  show("mix");
  cancelAnimationFrame(S.rafId); frame();
}
function refreshStrips() {
  const m = S.mix; if (!m) return;
  const anySolo = m.chs.some((c) => c.solo);
  m.chs.forEach((c) => {
    c.el.querySelector(".s").classList.toggle("on", c.solo);
    c.el.querySelector(".m").classList.toggle("on", c.mute);
    c.el.classList.toggle("off", !c.audible);
    c.stEl.textContent = anySolo && c.solo ? "SOLO" : !c.audible ? "MUTE" : "ON";
  });
  const k = $("#karaoke"); k.classList.toggle("on", m.karaokeOn); $("#karaoke-ico").textContent = m.karaokeOn ? "🔇" : "🎤";
}
function updatePlayBtn() { const p = $("#play"); const on = S.mix && S.mix.playing; p.innerHTML = on ? "&#10074;&#10074;" : "&#9654;"; p.setAttribute("aria-label", on ? "Pause" : "Play"); }

let seeking = false;
function frame() {
  S.rafId = requestAnimationFrame(frame);
  const m = S.mix; if (!m || S.screen !== "mix") return;
  const pos = m.pos(), prog = pos / m.duration;
  if (!seeking) { $("#seek").value = Math.round(prog * 1000); }
  $("#t-pos").textContent = fmt(pos);
  for (const c of m.chs) {
    let pk = 0;
    if (m.playing && c.audible) { c.an.getFloatTimeDomainData(c.data); for (let i = 0; i < c.data.length; i++) { const v = Math.abs(c.data[i]); if (v > pk) pk = v; } }
    c.level = Math.max(Math.min(1, pk * 1.4), (c.level || 0) * 0.85);
    c.meterEl.style.width = Math.round(c.level * 100) + "%";
    drawWave(c, prog);
  }
}
function drawWave(c, prog) {
  const cv = c.canvas, dpr = window.devicePixelRatio || 1;
  const w = Math.round(cv.clientWidth * dpr), h = Math.round(cv.clientHeight * dpr);
  if (!w || !h) return;
  if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
  const g = cv.getContext("2d"); g.clearRect(0, 0, w, h);
  const n = c.peaks.length, bw = w / n, col = CH[c.idx].color;
  for (let i = 0; i < n; i++) {
    const bh = Math.max(2 * dpr, c.peaks[i] * h * 0.92);
    g.globalAlpha = (c.audible ? 1 : 0.28) * (i / n <= prog ? 1 : 0.45);
    g.fillStyle = col; g.fillRect(i * bw + bw * 0.15, (h - bh) / 2, bw * 0.7, bh);
  }
  g.globalAlpha = 1; g.fillStyle = "#fff"; g.fillRect(Math.round(prog * w) - 1, 0, 2 * dpr, h);
}

$("#play").onclick = () => { const m = S.mix; if (!m) return; m.playing ? m.pause() : m.play(); updatePlayBtn(); };
$("#back5").onclick = () => S.mix && S.mix.seek(S.mix.pos() - 5);
$("#fwd5").onclick = () => S.mix && S.mix.seek(S.mix.pos() + 5);
$("#loop").onclick = () => { const m = S.mix; if (!m) return; m.setLoop(!m.loop); $("#loop").classList.toggle("on", m.loop); };
$("#seek").addEventListener("input", (e) => { seeking = true; $("#t-pos").textContent = fmt(e.target.value / 1000 * S.mix.duration); });
$("#seek").addEventListener("change", (e) => { S.mix.seek(e.target.value / 1000 * S.mix.duration); seeking = false; });
$("#karaoke").onclick = () => { S.mix.toggleKaraoke(); refreshStrips(); };
$("#mix-back").onclick = () => { if (S.mix) { S.mix.close(); S.mix = null; } cancelAnimationFrame(S.rafId); show("home"); };
document.addEventListener("keydown", (e) => {
  if (S.screen === "mix" && e.code === "Space" && !["INPUT", "BUTTON", "SELECT"].includes(document.activeElement.tagName)) { e.preventDefault(); $("#play").click(); }
});

// ---------------------------------------------------------------- export (WAV, ZIP when several files)
function wavBlob(int16Interleaved, channels) {
  const dataLen = int16Interleaved.length * 2, h = new DataView(new ArrayBuffer(44));
  const str = (o, s) => { for (let i = 0; i < s.length; i++) h.setUint8(o + i, s.charCodeAt(i)); };
  str(0, "RIFF"); h.setUint32(4, 36 + dataLen, true); str(8, "WAVE"); str(12, "fmt "); h.setUint32(16, 16, true);
  h.setUint16(20, 1, true); h.setUint16(22, channels, true); h.setUint32(24, SR, true); h.setUint32(28, SR * 2 * channels, true);
  h.setUint16(32, 2 * channels, true); h.setUint16(34, 16, true); str(36, "data"); h.setUint32(40, dataLen, true);
  return new Blob([h.buffer, int16Interleaved], { type: "audio/wav" });
}
const toI16 = (v) => (v < -1 ? -32768 : v > 1 ? 32767 : v < 0 ? v * 32768 : v * 32767);
function renderInterleaved(chans, gains) {
  const n = chans[0].buffer.length, out = new Int16Array(n * 2);
  const L = chans.map((c) => c.buffer.getChannelData(0)), R = chans.map((c) => c.buffer.getChannelData(1));
  for (let i = 0; i < n; i++) {
    let l = 0, r = 0;
    for (let k = 0; k < L.length; k++) { l += L[k][i] * gains[k]; r += R[k][i] * gains[k]; }
    out[2 * i] = toI16(l); out[2 * i + 1] = toI16(r);
  }
  return out;
}
let crcTable = null;
function crc32(u8) {
  if (!crcTable) { crcTable = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; crcTable[n] = c >>> 0; } }
  let c = 0xFFFFFFFF; for (let i = 0; i < u8.length; i++) c = crcTable[(c ^ u8[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
/** Minimal ZIP writer (no compression): files = [{ name, bytes: Uint8Array }] */
function zipBlob(files) {
  const enc = new TextEncoder(), parts = [], central = []; let offset = 0;
  for (const f of files) {
    const name = enc.encode(f.name), crc = crc32(f.bytes), size = f.bytes.length;
    const lh = new DataView(new ArrayBuffer(30));
    lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0x0800, true); lh.setUint16(8, 0, true);
    lh.setUint16(10, 0, true); lh.setUint16(12, 0x21, true); lh.setUint32(14, crc, true); lh.setUint32(18, size, true); lh.setUint32(22, size, true);
    lh.setUint16(26, name.length, true); lh.setUint16(28, 0, true);
    parts.push(lh.buffer, name, f.bytes);
    const ch = new DataView(new ArrayBuffer(46));
    ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true); ch.setUint16(8, 0x0800, true); ch.setUint16(10, 0, true);
    ch.setUint16(12, 0, true); ch.setUint16(14, 0x21, true); ch.setUint32(16, crc, true); ch.setUint32(20, size, true); ch.setUint32(24, size, true);
    ch.setUint16(28, name.length, true); ch.setUint32(42, offset, true);
    central.push(ch.buffer, name);
    offset += 30 + name.length + size;
  }
  const cdSize = central.reduce((a, p) => a + (p.byteLength !== undefined ? p.byteLength : p.length), 0);
  const end = new DataView(new ArrayBuffer(22));
  end.setUint32(0, 0x06054b50, true); end.setUint16(8, files.length, true); end.setUint16(10, files.length, true);
  end.setUint32(12, cdSize, true); end.setUint32(16, offset, true);
  return new Blob([...parts, ...central, end.buffer], { type: "application/zip" });
}
function download(blob, name) {
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 120000);
}

const exp = $("#exp");
$("#open-export").onclick = () => {
  const m = S.mix; if (!m) return;
  const list = $("#exp-list"); list.innerHTML = ""; $("#exp-msg").textContent = "";
  const add = (key, label, checked, color) => {
    const l = document.createElement("label"); l.className = "exp-item"; l.style.setProperty("--c", color);
    l.innerHTML = '<i class="dot"></i><span>' + label + '</span><input type="checkbox" data-k="' + key + '"' + (checked ? " checked" : "") + ">";
    list.appendChild(l);
  };
  if (m.chs.length > 1) add("mix", "Full mix (as set in the mixer)", false, "#00C78A");
  m.chs.forEach((c) => add("ch" + c.idx, CH[c.idx].label, true, CH[c.idx].color));
  exp.showModal();
};
$("#exp-close").onclick = () => exp.close();
$("#exp-go").onclick = async () => {
  const m = S.mix, picked = [...exp.querySelectorAll("input[type=checkbox]:checked")].map((i) => i.dataset.k);
  if (!picked.length) { $("#exp-msg").textContent = "Select at least one track."; return; }
  const go = $("#exp-go"); go.disabled = true;
  const tick = () => new Promise((r) => setTimeout(r, 20));
  try {
    const files = [], base = baseName(), anySolo = m.chs.some((c) => c.solo);
    for (const k of picked) {
      $("#exp-msg").textContent = "Preparing " + (k === "mix" ? "the full mix" : CH[+k.slice(2)].label) + "..."; await tick();
      if (k === "mix") {
        const gains = m.chs.map((c) => ((anySolo ? c.solo : !c.mute) ? c.vol / 0.7 : 0));
        if (gains.every((g) => g === 0)) { $("#exp-msg").textContent = "The mix is silent: unmute a track first."; go.disabled = false; return; }
        files.push({ name: base + "_mix.wav", blob: wavBlob(renderInterleaved(m.chs, gains), 2) });
      } else {
        const c = m.chs.find((x) => x.idx === +k.slice(2));
        files.push({ name: base + "_" + CH[c.idx].key + ".wav", blob: wavBlob(renderInterleaved([c], [1]), 2) });
      }
    }
    if (files.length === 1) download(files[0].blob, files[0].name);
    else {
      $("#exp-msg").textContent = "Creating the ZIP..."; await tick();
      const withBytes = [];
      for (const f of files) withBytes.push({ name: f.name, bytes: new Uint8Array(await f.blob.arrayBuffer()) });
      download(zipBlob(withBytes), base + "_stems.zip");
    }
    $("#exp-msg").textContent = "Done. Check your downloads.";
  } catch (err) { $("#exp-msg").textContent = "Export failed: " + err.message; }
  go.disabled = false;
};

// ---------------------------------------------------------------- start
show("home");
window.__app = S;   // handy for debugging in the console
