/*
 * Makes the page "cross-origin isolated" on hosts that cannot set headers (GitHub Pages), which the AI engine needs to use
 * several CPU threads. The first visit reloads once. Based on the well-known coi-serviceworker pattern.
 */
if (typeof window === "undefined") {
  self.addEventListener("install", () => self.skipWaiting());
  self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));
  // Only the splitter page needs cross-origin isolation. The information pages must stay without it so that ads can load.
  const isTool = (u) => { const p = new URL(u).pathname; return p.endsWith("/") || p.endsWith("/index.html"); };
  self.addEventListener("fetch", (e) => {
    const req = e.request;
    if (req.cache === "only-if-cached" && req.mode !== "same-origin") return;
    if (req.mode === "navigate" && !isTool(req.url)) return;          // information page: leave untouched
    e.respondWith((async () => {
      if (req.mode !== "navigate" && e.clientId) {
        const c = await self.clients.get(e.clientId);
        if (c && !isTool(c.url)) return fetch(req);                  // request of an information page (e.g. ads): untouched
      }
      try {
        const r = await fetch(req);
        if (r.status === 0) return r;
        const h = new Headers(r.headers);
        h.set("Cross-Origin-Embedder-Policy", "require-corp");
        h.set("Cross-Origin-Opener-Policy", "same-origin");
        return new Response(r.body, { status: r.status, statusText: r.statusText, headers: h });
      } catch (err) { console.error(err); return Response.error(); }
    })());
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
