(function () {
  // mobile menu
  var btn = document.getElementById('menuBtn'), nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var o = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', o);
    });
  }

  // enquiry forms (preview only - not connected to an inbox yet)
  document.querySelectorAll('form.enquiry').forEach(function (form) {
    var note = form.querySelector('.form-note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = (form.elements.first || {}).value || '';
      var phone = (form.elements.phone || {}).value || '';
      if (!first.trim() || !phone.trim()) {
        note.className = 'note form-note';
        note.textContent = 'Please add your first name and phone number so our team can call you back.';
        return;
      }
      note.className = 'ok form-note';
      note.textContent = 'Thank you, ' + first.trim() + '. This is a website preview, so the enquiry was not sent. Once the form is connected to the Vitania Care inbox, enquiries will arrive there.';
    });
  });

  // copy buttons for emails
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var text = b.getAttribute('data-copy');
      var done = function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1500); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { select(b); });
      } else { select(b); }
    });
  });
  function select(b) {
    var t = b.previousElementSibling; if (!t) return;
    var r = document.createRange(); r.selectNodeContents(t);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }
})();

(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // scroll progress bar
  var bar = document.createElement('div'); bar.className = 'progress'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  var cssProgress = window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()');

  // back-to-top button
  var top = document.createElement('button');
  top.className = 'to-top'; top.type = 'button'; top.setAttribute('aria-label', 'Back to top');
  top.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
  document.body.appendChild(top);

  var header = document.querySelector('header.site');
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    if (header) header.classList.toggle('scrolled', y > 24);
    top.classList.toggle('show', y > 600);
    if (!cssProgress) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // mark elements that rise into view as you scroll
  var sel = '.head, .tile, .group, .person, .perk, .svc-art, .svc-body, .steps li, .faq details, .statement, .cta-banner, form.enquiry, .info dl';
  document.querySelectorAll(sel).forEach(function (el) {
    if (!el.closest('.page-hero') && !el.closest('.hero')) el.classList.add('reveal');
  });

  // close mobile menu after choosing a link
  var nav = document.getElementById('nav'), btn = document.getElementById('menuBtn');
  if (nav && btn) nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  });
})();
