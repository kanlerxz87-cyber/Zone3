// Minimal enhancement: live filter for any data table that has a preceding wrapper.
// The site is fully readable without JavaScript.
(function () {
  document.querySelectorAll('table.data').forEach(function (table) {
    var wrap = table.parentElement;
    if (!wrap || !wrap.classList.contains('tablewrap') || table.tBodies.length === 0) return;
    if (table.tBodies[0].rows.length < 4) return;
    var input = document.createElement('input');
    input.type = 'search';
    input.placeholder = 'Filter rows…';
    input.id = 'filter';
    input.setAttribute('aria-label', 'Filter table rows');
    wrap.parentElement.insertBefore(input, wrap);
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      Array.prototype.forEach.call(table.tBodies[0].rows, function (r) {
        r.style.display = !q || r.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
      });
    });
  });
})();
