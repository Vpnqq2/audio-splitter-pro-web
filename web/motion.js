/* Scroll-reveal for sections. Content stays visible without JS or with reduced motion. */
(function () {
  if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var sel = ".sec-title,.feat,.stems-show>*,.steps>li,.uses>li,.faq,.band,.promo,.guide-card,.gcard,.cards>*,.tool-card,.sec-wave";
  var els = Array.prototype.slice.call(document.querySelectorAll(sel)).filter(function (e) {
    return e.getBoundingClientRect().top > innerHeight * 0.9;
  });
  var io = new IntersectionObserver(function (list) {
    list.forEach(function (x) {
      if (!x.isIntersecting) return;
      var e = x.target; io.unobserve(e); e.classList.add("in");
      setTimeout(function () { e.classList.remove("rv", "in"); e.style.removeProperty("--d"); }, 1100);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
  els.forEach(function (e) {
    var sib = e.parentNode ? Array.prototype.indexOf.call(e.parentNode.children, e) : 0;
    e.style.setProperty("--d", Math.min(sib, 5) * 80 + "ms");
    e.classList.add("rv"); io.observe(e);
  });
})();
