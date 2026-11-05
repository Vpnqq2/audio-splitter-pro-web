/* Runs the AI model (HT-Demucs, ONNX) off the main thread. Same algorithm as the Android app. */
"use strict";
const ORT_BASE = "https://cdn.jsdelivr.net/npm/onnxruntime-web@1.22.0/dist/";
const MODEL_URL = "https://huggingface.co/Moussa007/Mousic/resolve/main/htdemucs_fp16weights.onnx";
const MODEL_SIZE = 165612636;   // used for the progress bar when the server does not say
const CACHE_NAME = "demucs-model-v1";
const CHUNK = 343980;           // model input: [1, 2, 343980] at 44.1 kHz

let ortOk = true;
function loadOrt(gpu) {   // the plain build is lighter; the WebGPU build only when asked for
  try { importScripts(ORT_BASE + (gpu ? "ort.webgpu.min.js" : "ort.min.js")); ort.env.wasm.wasmPaths = ORT_BASE; ortOk = true; } catch (e) { ortOk = false; }
}

let session = null;
const post = (m, t) => postMessage(m, t || []);

onmessage = async (e) => {
  try {
    if (e.data.type === "init") await init(e.data);
    else if (e.data.type === "run") await run(e.data);
  } catch (err) {
    post({ type: "error", message: String((err && err.message) || err).slice(0, 120), retry: !!(err && err.retry) || (e.data.type === "run") });
  }
};

async function getModelBytes() {
  let cache = null;
  try { cache = await caches.open(CACHE_NAME); } catch (_) {}
  if (cache) {
    const hit = await cache.match(MODEL_URL);
    if (hit) {
      post({ type: "status", text: "Loading the AI engine from this device..." });
      const buf = await hit.arrayBuffer();
      if (buf.byteLength > 100 * 1024 * 1024) return new Uint8Array(buf);
      await cache.delete(MODEL_URL);   // damaged copy: download again
    }
  }
  post({ type: "status", text: "Downloading the AI engine (first time only, about 165 MB)..." });
  const resp = await fetch(MODEL_URL);
  if (!resp.ok) throw new Error("The AI engine could not be downloaded (HTTP " + resp.status + ").");
  const total = Number(resp.headers.get("content-length")) || MODEL_SIZE;
  const reader = resp.body.getReader();
  const parts = []; let got = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    parts.push(value); got += value.length;
    post({ type: "download", p: Math.min(1, got / total) });
  }
  if (got < 100 * 1024 * 1024) throw new Error("The AI engine download was incomplete. Please try again.");
  const blob = new Blob(parts);
  parts.length = 0;
  if (cache) { try { await cache.put(MODEL_URL, new Response(blob, { headers: { "content-length": String(got) } })); } catch (_) {} }
  return new Uint8Array(await blob.arrayBuffer());
}

async function init({ gpu, threads, safe }) {
  if (session) { post({ type: "ready", gpu: false }); return; }
  loadOrt(gpu);
  if (!ortOk) throw new Error("Could not load the AI runtime. Check your internet connection and reload the page.");
  let bytes = await getModelBytes();
  post({ type: "status", text: "Starting the AI engine..." });
  // light modes: no graph optimisation (it needs extra memory) and no memory arena
  const opts = safe
    ? { executionProviders: ["wasm"], graphOptimizationLevel: "disabled", enableCpuMemArena: false, enableMemPattern: false }
    : { executionProviders: ["wasm"], graphOptimizationLevel: "all" };
  ort.env.wasm.numThreads = Math.max(1, threads | 0);
  let usedGpu = false;
  if (gpu) {
    try {
      session = await ort.InferenceSession.create(bytes, { executionProviders: ["webgpu"], graphOptimizationLevel: "all" });
      usedGpu = true;
    } catch (err) { session = null; }
  }
  if (!session) {
    try { session = await ort.InferenceSession.create(bytes, opts); }
    catch (err) { const e = new Error("start: " + String((err && err.message) || err)); e.retry = true; throw e; }
  }
  bytes = null;
  post({ type: "ready", gpu: usedGpu, threads: usedGpu ? 0 : ort.env.wasm.numThreads, isolated: !!self.crossOriginIsolated, safe: !!safe });
}

async function run({ left, right, stems, div }) {
  const total = left.length;
  const overlap = Math.floor(CHUNK / div);
  const hop = CHUNK - overlap;
  const steps = Math.max(1, Math.ceil((total - overlap) / hop));
  const out = stems.map(() => [new Int16Array(total), new Int16Array(total)]);
  const tail = stems.map(() => [new Float32Array(overlap), new Float32Array(overlap)]);
  const x = new Float32Array(2 * CHUNK);
  const silent = new Float32Array(4 * 2 * CHUNK);
  const inName = session.inputNames[0], outName = session.outputNames[0];
  const t0 = performance.now();

  for (let step = 0; step < steps; step++) {
    const start = step * hop;
    let peak = 0;
    for (let i = 0; i < CHUNK; i++) {
      const s = start + i;
      if (s < total) {
        const l = left[s], r = right[s];
        x[i] = l; x[CHUNK + i] = r;
        const a = Math.max(Math.abs(l), Math.abs(r)); if (a > peak) peak = a;
      } else { x[i] = 0; x[CHUNK + i] = 0; }
    }
    let y = silent;                       // digital silence: skip the heavy model call
    if (peak >= 1e-4) {
      const input = new ort.Tensor("float32", x, [1, 2, CHUNK]);
      let res;
      try { res = await session.run({ [inName]: input }); }
      catch (err) { throw new Error("run: " + String((err && err.message) || err)); }
      y = res[outName].data;
      try { res[outName].dispose(); } catch (_) {}
    }
    const last = step === steps - 1;
    const keep = last ? Math.min(CHUNK, total - start) : hop;
    for (let k = 0; k < stems.length; k++) {
      const s = stems[k];
      for (let c = 0; c < 2; c++) {
        const base = (s * 2 + c) * CHUNK, dst = out[k][c], tl = tail[k][c];
        for (let i = 0; i < keep; i++) {
          let v = y[base + i];
          if (step > 0 && i < overlap) { const w = i / overlap; v = v * w + tl[i] * (1 - w); }
          v = v < -1 ? -1 : v > 1 ? 1 : v;
          dst[start + i] = v < 0 ? v * 32768 : v * 32767;
        }
        if (!last) for (let i = 0; i < overlap; i++) tl[i] = y[base + hop + i];
      }
    }
    const p = (step + 1) / steps;
    const el = (performance.now() - t0) / 1000;
    post({ type: "progress", p, eta: p > 0.04 ? Math.round(el * (1 - p) / p) : 0 });
  }
  const result = stems.map((s, k) => ({ stem: s, left: out[k][0], right: out[k][1] }));
  post({ type: "done", stems: result }, result.flatMap((r) => [r.left.buffer, r.right.buffer]));
}
