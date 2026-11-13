/* Zone3 dashboard behaviour: row filter + column sort. No network calls.
   Deliberately zero runtime fetching: Program Content must not be stored or
   cached by a client application (Associates Program IP License 2(h)), so every
   value on these pages is baked into the HTML at build time. */
(function () {
  "use strict";

  function rowsOf(table) {
    return Array.prototype.slice.call(table.tBodies[0].rows);
  }

  /* ---- filter ---- */
  document.querySelectorAll("[data-table-filter]").forEach(function (input) {
    var wrap = input.closest(".tbl-head");
    var card = wrap && wrap.parentNode;
    if (!card) return;
    var table = card.querySelector("table");
    if (!table || !table.tBodies.length) return;
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      rowsOf(table).forEach(function (tr) {
        var hit = !q || tr.textContent.toLowerCase().indexOf(q) !== -1;
        tr.hidden = !hit;
        if (hit) shown++;
      });
      var note = card.querySelector(".filter-count");
      if (!note) {
        note = document.createElement("p");
        note.className = "note filter-count";
        card.appendChild(note);
      }
      note.textContent = q ? shown + " of " + rowsOf(table).length + " rows match “" + input.value + "”" : "";
    });
  });

  /* ---- sort ---- */
  document.querySelectorAll("table").forEach(function (table) {
    if (!table.tHead || !table.tBodies.length) return;
    Array.prototype.forEach.call(table.tHead.rows[0].cells, function (th, idx) {
      if (th.className.indexOf("nosort") !== -1) return;
      th.setAttribute("title", "Sort by " + th.textContent.trim());
      th.tabIndex = 0;
      function run() {
        var dir = th.getAttribute("data-dir") === "asc" ? "desc" : "asc";
        Array.prototype.forEach.call(table.tHead.rows[0].cells, function (c) {
          c.removeAttribute("data-dir");
        });
        th.setAttribute("data-dir", dir);
        var rows = rowsOf(table);
        rows.sort(function (a, b) {
          var ax = (a.cells[idx] ? a.cells[idx].textContent : "").trim();
          var bx = (b.cells[idx] ? b.cells[idx].textContent : "").trim();
          var an = parseFloat(ax.replace(/[^0-9.\-]/g, ""));
          var bn = parseFloat(bx.replace(/[^0-9.\-]/g, ""));
          var cmp;
          if (!isNaN(an) && !isNaN(bn)) cmp = an - bn;
          else cmp = ax.localeCompare(bx, undefined, { numeric: true, sensitivity: "base" });
          return dir === "asc" ? cmp : -cmp;
        });
        var frag = document.createDocumentFragment();
        rows.forEach(function (r) { frag.appendChild(r); });
        table.tBodies[0].appendChild(frag);
      }
      th.addEventListener("click", run);
      th.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); run(); }
      });
    });
  });

  /* ---- external links: mark them so a reader can see they leave the site ---- */
  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    var here = location.host.indexOf("github.io") !== -1 &&
               a.host.indexOf("github.io") !== -1 &&
               a.pathname.split("/")[1] === location.pathname.split("/")[1];
    if (!here && a.hostname !== location.hostname) {
      a.setAttribute("data-external", "");
      a.addEventListener("mouseenter", function () {
        a.title = (a.title ? a.title + " · " : "") + "Opens " + a.hostname;
      });
    }
  });
})();
