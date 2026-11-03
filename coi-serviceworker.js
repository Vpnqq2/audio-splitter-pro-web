/*
 * Makes the page "cross-origin isolated" on hosts that cannot set headers (GitHub Pages), which the AI engine needs to use
 * several CPU threads. The first visit reloads once. Based on the well-known coi-serviceworker pattern.
 */
if (typeof window === "undefined") {
  self.addEventListener("install", () => self.skipWaiting());
  self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));
  self.addEventListener("fetch", (e) => {
    if (e.request.cache === "only-if-cached" && e.request.mode !== "same-origin") return;
    e.respondWith(
      fetch(e.request).then((r) => {
        if (r.status === 0) return r;
        const h = new Headers(r.headers);
        h.set("Cross-Origin-Embedder-Policy", "require-corp");
        h.set("Cross-Origin-Opener-Policy", "same-origin");
        return new Response(r.body, { status: r.status, statusText: r.statusText, headers: h });
      }).catch((err) => console.error(err))
    );
  });
} else {
  (async () => {
    if (window.crossOriginIsolated !== false || !window.isSecureContext || !("serviceWorker" in navigator)) return;
    try {
      const reg = await navigator.serviceWorker.register(window.document.currentScript.src);
      reg.addEventListener("updatefound", () => window.location.reload());
      if (reg.active && !navigator.serviceWorker.controller) window.location.reload();
    } catch (e) { console.warn("coi service worker failed", e); }
  })();
}
