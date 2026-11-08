(function () {
  var btn = document.getElementById('menuBtn'), nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Enquiry forms post to FormSubmit, which emails each enquiry to the Vitania Care inbox.
  document.querySelectorAll('form.enquiry').forEach(function (form) {
    var next = form.querySelector('input[name="_next"]');
    if (next) next.value = location.origin + location.pathname.replace(/[^/]*$/, '') + 'thank-you.html';
  });

  // Scroll reveal: items appear one after another as they come into view.
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('js');
    var groups = [
      ['.head', ''], ['.pillars li', ''], ['.cards .card', ''], ['.features .feature', ''],
      ['.steps li', ''], ['.faq details', ''], ['.team .person', ''], ['.vm > div', ''],
      ['.split .media', 'zoom'], ['.split .copy', ''], ['.benefits li', 'from-left'], ['.chips li', ''],
      ['.cta', 'zoom'], ['.audience .aud', 'zoom'], ['.info', 'from-left'], ['form.enquiry', 'from-right'], ['.foot > div', '']
    ];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (el) {
        if (el.closest('.hero') || el.closest('.page-hero')) return;
        var sibs = Array.prototype.filter.call(el.parentNode.children, function (c) { return c.matches(g[0]); });
        el.style.setProperty('--d', (Math.min(sibs.indexOf(el), 6) * 0.12) + 's');
        el.classList.add('reveal'); if (g[1]) el.classList.add(g[1]);
        io.observe(el);
      });
    });
  }

  var top = document.createElement('button');
  top.className = 'to-top'; top.type = 'button'; top.setAttribute('aria-label', 'Back to top');
  top.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  document.body.appendChild(top);
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () { top.classList.toggle('show', window.scrollY > 700); ticking = false; });
  }, { passive: true });
})();
