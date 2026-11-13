/* Zone3 Affiliate Intelligence — tiny progressive enhancements (no dependencies) */
(function () {
  // Highlight active nav link based on pathname
  var path = (location.pathname.split('/').pop() || 'index.html');
  document.querySelectorAll('.sidebar nav a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === path || (path === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });

  // Client-side table filter (products / sources tables)
  document.querySelectorAll('[data-filter-target]').forEach(function (input) {
    var table = document.querySelector(input.getAttribute('data-filter-target'));
    if (!table) return;
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      table.querySelectorAll('tbody tr').forEach(function (row) {
        row.style.display = !q || row.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
      });
    });
  });
})();
