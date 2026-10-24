/* Explicit language in URL wins over saved preference and browser language. */
(function () {
  'use strict';
  var supported = ['fr', 'en', 'es', 'pt'];
  function normalise(value) {
    var code = String(value || '').toLowerCase().split(/[-_]/)[0];
    return supported.indexOf(code) >= 0 ? code : null;
  }
  var current = new URL(window.location.href);
  var pathLanguage = normalise(current.pathname.split('/')[1]);
  var selected;
  try { selected = normalise(localStorage.getItem('capsoa.language')); } catch (_) {}
  if (!pathLanguage) {
    var language = normalise(current.searchParams.get('lang')) || selected;
    if (!language) {
      (navigator.languages || [navigator.language]).some(function (item) {
        language = normalise(item); return Boolean(language);
      });
    }
    language = language || 'fr';
    var name = current.pathname.replace(/^\//, '').replace(/\.html$/, '');
    if (name === 'index') name = '';
    if (['', 'cgu', 'cgv', 'mentions-legales', 'conditions-mineurs', 'politique-confidentialite', 'suppression-compte'].indexOf(name) >= 0) {
      current.pathname = '/' + language + '/' + name;
      current.searchParams.delete('lang');
      window.location.replace(current.href);
      return;
    }
  } else {
    try { localStorage.setItem('capsoa.language', pathLanguage); } catch (_) {}
  }
  document.querySelectorAll('[data-language]').forEach(function (link) {
    var target = new URL(link.href);
    target.hash = current.hash;
    link.href = target.href;
    link.addEventListener('click', function () {
      try { localStorage.setItem('capsoa.language', link.dataset.language); } catch (_) {}
    });
  });
}());
