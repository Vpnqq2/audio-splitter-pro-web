/* Loads Google AdSense on information pages, only after the visitor has chosen (or Google's own consent message handles it). */
(function () {
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
    var b = document.createElement("div"); b.className = "consent"; b.setAttribute("role", "dialog");
    b.innerHTML = '<span>This page can show ads. Google and its partners may use cookies to personalise them. You can accept, or choose non-personalised ads. <a href="privacy.html">Privacy policy</a></span><div><button class="ok">Accept</button><button class="no">Non-personalised</button></div>';
    b.querySelector(".ok").onclick = function () { put("yes"); b.remove(); load(true); };
    b.querySelector(".no").onclick = function () { put("no"); b.remove(); load(false); };
    document.body.appendChild(b);
  }
  if (!C.client) return;                       // no ads configured: nothing to do
  if (C.googleCmp) { load(true); return; }     // Google's message does the asking
  var link = document.getElementById("ad-choices");
  if (link) { link.hidden = false; link.onclick = function (e) { e.preventDefault(); banner(); }; }
  var v = get();
  if (v === "yes") load(true); else if (v === "no") load(false); else banner();
})();
