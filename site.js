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

  var sel = '.card, .feature, .steps li, .faq details, .person, .split .media, .cta';
  document.querySelectorAll(sel).forEach(function (el) { el.classList.add('reveal'); });

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
