/* Shared by every page: mobile menu. On information pages it also loads Google AdSense, only after the visitor has chosen. */
(function () {
  var b = document.getElementById("burger"), n = document.getElementById("nav");
  if (b && n) {
    var set = function (o) { n.classList.toggle("open", o); b.setAttribute("aria-expanded", o ? "true" : "false"); };
    b.addEventListener("click", function (e) { e.stopPropagation(); set(!n.classList.contains("open")); });
    document.addEventListener("click", function (e) { if (n.classList.contains("open") && !n.contains(e.target) && !b.contains(e.target)) set(false); });
    n.addEventListener("click", function (e) { if (e.target.tagName === "A") set(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") set(false); });
  }
  if (document.body.hasAttribute("data-noads")) return;   // the splitter page never shows ads
  var C = window.ADS || {};
  function get() { try { return localStorage.getItem("ads_consent"); } catch (e) { return null; } }
  function put(v) { try { localStorage.setItem("ads_consent", v); } catch (e) {} }
  function load(personal) {
    if (!C.client || window.__adsLoaded) return;
    window.__adsLoaded = true;
    var q = (window.adsbygoogle = window.adsbygoogle || []);
    if (!personal && !C.googleCmp) q.requestNonPersonalizedAds = 1;
    var s = document.createElement("script");
    s.async = true; s.crossOrigin = "anonymous";
    s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + encodeURIComponent(C.client);
    document.head.appendChild(s);
  }
  function banner() {
    if (document.querySelector(".consent")) return;
    var d = document.createElement("div"); d.className = "consent"; d.setAttribute("role", "dialog"); d.setAttribute("aria-label", "Advertising choices");
    d.innerHTML = '<span>This page can show ads. Google and its partners may use cookies to personalise them. You can accept, or choose non-personalised ads. <a href="privacy.html">Privacy Policy</a></span><div><button class="ok">Accept</button><button class="no">Non-personalised</button></div>';
    d.querySelector(".ok").onclick = function () { put("yes"); d.remove(); load(true); };
    d.querySelector(".no").onclick = function () { put("no"); d.remove(); load(false); };
    document.body.appendChild(d);
  }
  if (!C.client) return;
  if (C.googleCmp) { load(true); return; }
  var link = document.getElementById("ad-choices");
  if (link) { link.hidden = false; link.onclick = function (e) { e.preventDefault(); banner(); }; }
  var v = get();
  if (v === "yes") load(true); else if (v === "no") load(false); else banner();
})();
