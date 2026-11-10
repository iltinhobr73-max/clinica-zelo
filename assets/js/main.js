/* Clínica Zelo — comportamento mínimo: cabeçalho, menu do celular, aparição ao rolar, barra inferior. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var header = document.querySelector("[data-header]");
  var dock = document.querySelector("[data-dock]");

  /* Cabeçalho compacto e barra inferior, conforme a rolagem */
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-stuck", y > 24);
    if (dock) dock.classList.toggle("is-on", y > 480);
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  /* Menu em tela cheia (celular e tablet) */
  var btn = document.querySelector("[data-menu-btn]");
  var menu = document.getElementById("menu");
  if (btn && menu) {
    var label = btn.querySelector("[data-menu-label]");
    var setOpen = function (open) {
      btn.setAttribute("aria-expanded", String(open));
      if (label) label.textContent = open ? "Fechar" : "Menu";
      menu.classList.toggle("is-open", open);
      if (open) { menu.removeAttribute("inert"); } else { menu.setAttribute("inert", ""); }
      document.body.classList.toggle("menu-open", open);
      if (open) { var first = menu.querySelector("a"); if (first) first.focus(); }
    };
    setOpen(false);
    btn.addEventListener("click", function () { setOpen(btn.getAttribute("aria-expanded") !== "true"); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { setOpen(false); btn.focus(); }
    });
    window.matchMedia("(min-width: 64rem)").addEventListener("change", function (e) { if (e.matches) setOpen(false); });
  }

  /* Aparição suave, uma única vez */
  var items = document.querySelectorAll(".reveal");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }
  doc.classList.add("js-ready");
})();
