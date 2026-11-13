/* Zone3 dashboard client behaviours.
   Nothing here invents data: it only filters, sorts and copies values that are
   already present in the DOM. */
(function () {
  "use strict";

  /* ---------------------------------------------------------- table filter */
  document.querySelectorAll("[data-filter]").forEach(function (input) {
    var sel = input.getAttribute("data-filter");
    var table = document.querySelector(sel);
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      rows.forEach(function (r) {
        r.style.display = q === "" || r.textContent.toLowerCase().indexOf(q) !== -1 ? "" : "none";
      });
    });
  });

  /* ------------------------------------------------------- copy to clipboard */
  function flash(btn, msg) {
    var old = btn.textContent;
    btn.textContent = msg;
    setTimeout(function () { btn.textContent = old; }, 1400);
  }
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var src = document.querySelector(btn.getAttribute("data-copy"));
      if (!src) return;
      var text = src.value !== undefined ? src.value : src.textContent;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { flash(btn, "copied"); });
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        flash(btn, "copied");
      }
    });
  });

  /* ------------------------------------------------------------ link builder */
  var form = document.getElementById("lb-form");
  if (form) {
    var out = document.getElementById("lb-out");
    var warn = document.getElementById("lb-warn");
    var catalog = window.ZONE3_PRODUCTS || [];

    var sel = document.getElementById("lb-asin");
    catalog.forEach(function (p) {
      var o = document.createElement("option");
      o.value = p.asin;
      o.textContent = p.asin + "  —  " + p.title.slice(0, 58) + (p.title.length > 58 ? "…" : "");
      sel.appendChild(o);
    });

    var TAG_RE = /^[A-Za-z0-9]+-20$/;

    function build() {
      var asin = sel.value;
      var tag = document.getElementById("lb-tag").value.trim();
      var extra = document.getElementById("lb-extra").value.trim();
      var base = "https://www.amazon.com/dp/" + asin;

      if (!tag) {
        out.textContent = base;
        warn.innerHTML = '<span class="tag t-bad">no tag</span> This is a plain product link. '
          + 'Amazon requires your Associates ID to appear as a parameter in every Special Link, '
          + 'so no commission can accrue until a tag is entered.';
        return;
      }
      if (!TAG_RE.test(tag)) {
        out.textContent = base + "?tag=" + tag;
        warn.innerHTML = '<span class="tag t-warn">check format</span> Amazon tags normally look like '
          + '<span class="mono">yourname-20</span> (letters/digits, then a dash, then <span class="mono">-20</span> '
          + 'for US accounts). The link was built anyway — copy the tag exactly as it appears in Associates Central.';
        return;
      }

      var url = base + "?tag=" + encodeURIComponent(tag);
      if (extra) {
        url += (extra.indexOf("?") === 0 || extra.indexOf("&") === 0) ? extra : "&" + extra;
        url = url.replace("?tag=", "?" + "").replace("&&", "&");
        // rebuild cleanly to avoid a messy query string
        url = base + "?" + (extra.replace(/^[?&]/, "") ? extra.replace(/^[?&]/, "") + "&" : "")
              + "tag=" + encodeURIComponent(tag);
      }
      out.textContent = url;
      warn.innerHTML = '<span class="tag t-ok">ready</span> Open this link directly from a page on your own '
        + 'site. Amazon requires Special Links to be accessed directly from your Site, and you must not ask '
        + 'visitors to bookmark them.';
    }

    form.addEventListener("input", build);
    form.addEventListener("submit", function (ev) { ev.preventDefault(); });
    build();
  }
})();
