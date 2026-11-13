/* Zone3 site — small, dependency-free dashboard behaviours. */
(function () {
  'use strict';

  /* ---- mobile sidebar ---- */
  var sidebar = document.getElementById('sidebar');
  var burger = document.querySelector('.burger');
  if (burger && sidebar) {
    burger.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!sidebar.classList.contains('open')) return;
      if (sidebar.contains(e.target) || burger.contains(e.target)) return;
      sidebar.classList.remove('open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') sidebar.classList.remove('open');
    });
  }

  /* ---- sortable tables ---- */
  document.querySelectorAll('table[data-sortable]').forEach(function (table) {
    var tbody = table.tBodies[0];
    if (!tbody) return;
    var headers = Array.prototype.slice.call(table.tHead ? table.tHead.querySelectorAll('th[data-sort]') : []);
    var dir = {};

    headers.forEach(function (th, idx) {
      th.setAttribute('scope', 'col');
      th.setAttribute('aria-sort', 'none');
      th.addEventListener('click', function () {
        var kind = th.getAttribute('data-sort') || 'text';
        var prev = dir[idx];
        dir[idx] = prev === 'asc' ? 'desc' : 'asc';
        var mult = dir[idx] === 'asc' ? 1 : -1;

        headers.forEach(function (other, j) {
          other.setAttribute('aria-sort', j === idx ? (dir[idx] === 'asc' ? 'ascending' : 'descending') : 'none');
        });

        var rows = Array.prototype.slice.call(tbody.rows);
        rows.sort(function (a, b) {
          var ra = a.cells[idx], rb = b.cells[idx];
          if (!ra || !rb) return 0;
          var va = (ra.getAttribute('data-v') || ra.textContent || '').trim();
          var vb = (rb.getAttribute('data-v') || rb.textContent || '').trim();
          if (kind === 'num') {
            var na = parseFloat(va.replace(/[^0-9.\-]/g, ''));
            var nb = parseFloat(vb.replace(/[^0-9.\-]/g, ''));
            if (isNaN(na)) na = -Infinity;
            if (isNaN(nb)) nb = -Infinity;
            return (na - nb) * mult;
          }
          return va.localeCompare(vb, undefined, { numeric: true, sensitivity: 'base' }) * mult;
        });
        rows.forEach(function (r) { tbody.appendChild(r); });
      });
    });
  });

  /* ---- product filter ---- */
  var search = document.querySelector('input[data-filter]');
  if (search) {
    var target = document.querySelector(search.getAttribute('data-filter'));
    if (target) {
      var rows = Array.prototype.slice.call(target.tBodies[0].rows);
      search.addEventListener('input', function () {
        var q = search.value.toLowerCase().trim();
        rows.forEach(function (r) {
          r.style.display = !q || r.textContent.toLowerCase().indexOf(q) > -1 ? '' : 'none';
        });
      });
    }
  }

  /* ---- flag severity filter ---- */
  var pills = document.querySelectorAll('.pill[data-sev]');
  if (pills.length) {
    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        var sev = pill.getAttribute('data-sev');
        pills.forEach(function (p) { p.classList.toggle('on', p === pill); });
        document.querySelectorAll('[data-flag-row]').forEach(function (row) {
          var show = sev === 'all' || row.getAttribute('data-flag-row') === sev;
          row.style.display = show ? '' : 'none';
        });
      });
    });
  }
})();
