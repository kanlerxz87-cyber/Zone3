/* Zone3 Kitchen: progressive enhancement only. No third-party libraries or tracking.
 * Product/category filters, local search and explicit local review/export.
 * An editorial review never publishes or changes configuration.
 */
(function () {
  'use strict';
  if (window.__zone3PublicationReady) return;
  window.__zone3PublicationReady = true;
  document.documentElement.classList.add('p26-js');

  function all(selector, root) { return Array.prototype.slice.call((root || document).querySelectorAll(selector)); }
  var nav = document.getElementById('p26-primary');
  var menu = document.querySelector('.p26-menu-toggle');
  if (menu && nav) {
    menu.addEventListener('click', function () {
      var expanded = menu.getAttribute('aria-expanded') === 'true';
      menu.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('is-open', !expanded);
    });
  }
  all('.p26-workspace').forEach(function (details) {
    document.addEventListener('click', function (event) {
      if (!details.contains(event.target)) details.open = false;
    });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    // A search input consumes the first native Escape to clear its value in Chromium.
    // Close explicitly so keyboard users always dismiss the modal in one press.
    if (dialog && dialog.open) { event.preventDefault(); dialog.close(); return; }
    var open = document.querySelector('.p26-workspace[open]');
    if (open) { open.open = false; open.querySelector('summary').focus(); }
    if (menu && nav && nav.classList.contains('is-open')) {
      nav.classList.remove('is-open'); menu.setAttribute('aria-expanded', 'false'); menu.focus();
    }
  });

  function filterButtons(selector, cardSelector, attribute, liveId) {
    var buttons = all(selector);
    var cards = all(cardSelector);
    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        var selected = button.getAttribute(attribute);
        buttons.forEach(function (other) {
          var active = button === other;
          other.setAttribute('aria-pressed', String(active)); other.classList.toggle('is-active', active);
        });
        var count = 0;
        cards.forEach(function (card) {
          var value = card.getAttribute(attribute === 'data-filter' ? 'data-category' : 'data-priority');
          card.hidden = selected !== 'all' && value !== selected;
          if (!card.hidden) count += 1;
        });
        var status = liveId && document.getElementById(liveId);
        if (status) status.textContent = count + ' products shown' + (selected === 'all' ? '.' : ' in ' + (selected === 'air-fryers' ? 'air fryers.' : 'thermometers.'));
      });
    });
  }
  filterButtons('[data-filter]', '[data-product-card]', 'data-filter', 'p26-filter-status');
  filterButtons('[data-proposal-filter]', '[data-proposal]', 'data-proposal-filter', '');

  var dialog = document.getElementById('p26-search');
  var query = document.getElementById('p26-query');
  var results = document.getElementById('p26-search-results');
  var opener = null;
  var index = null;
  var searchPromise = null;
  function renderSearch() {
    if (!results || !index) return;
    results.replaceChildren();
    var terms = (query.value || '').trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    var matches = index.filter(function (item) {
      var text = (item.title + ' ' + item.description + ' ' + item.kind).toLocaleLowerCase();
      return terms.every(function (term) { return text.indexOf(term) !== -1; });
    }).slice(0, 11);
    if (!matches.length) {
      var empty = document.createElement('p');
      empty.className = 'p26-search-empty'; empty.textContent = 'No match yet. Try “basket”, “capacity”, “cleanup” or “thermometer”.';
      results.appendChild(empty); return;
    }
    matches.forEach(function (item) {
      // Public build data only. Refuse absolute or path-traversing targets even if the index is corrupted.
      if (!/^(guides|shop)\/[A-Za-z0-9_/#.\-]+$/.test(item.path) || item.path.indexOf('..') !== -1) return;
      var link = document.createElement('a');
      link.href = dialog.getAttribute('data-root') + item.path;
      var label = document.createElement('span'); label.className = 'p26-overline'; label.textContent = item.kind;
      var title = document.createElement('strong'); title.textContent = item.title;
      var description = document.createElement('span'); description.textContent = item.description;
      link.appendChild(label); link.appendChild(title); link.appendChild(description); results.appendChild(link);
    });
  }
  function getIndex() {
    if (index) { renderSearch(); return; }
    if (searchPromise) return;
    results.textContent = 'Opening the reading room…';
    searchPromise = fetch(dialog.getAttribute('data-search-index'), { credentials: 'omit', referrerPolicy: 'no-referrer' })
      .then(function (response) { if (!response.ok) throw new Error('search unavailable'); return response.json(); })
      .then(function (data) { if (!Array.isArray(data)) throw new Error('bad index'); index = data; renderSearch(); })
      .catch(function () {
        results.replaceChildren(); var p = document.createElement('p'); p.textContent = 'Search is unavailable right now. Every guide is still in the reading room.';
        var a = document.createElement('a'); a.href = dialog.getAttribute('data-root') + 'guides/index.html'; a.textContent = 'Browse all guides →';
        results.appendChild(p); results.appendChild(a); searchPromise = null;
      });
  }
  if (dialog && typeof dialog.showModal === 'function') {
    all('[data-search-open]').forEach(function (link) {
      link.addEventListener('click', function (event) {
        event.preventDefault(); opener = link; dialog.showModal(); query.focus(); getIndex();
      });
    });
    all('[data-search-close]', dialog).forEach(function (button) { button.addEventListener('click', function () { dialog.close(); }); });
    dialog.addEventListener('click', function (event) { if (event.target === dialog) { var box = dialog.getBoundingClientRect(); if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close(); } });
    dialog.addEventListener('close', function () { if (opener) opener.focus(); });
    query.addEventListener('input', renderSearch);
  }

  var storageKey = 'zone3-publication-review-v1';
  var selects = all('[data-decision-id]');
  var status = document.getElementById('p26-review-status');
  var validChoices = ['unreviewed', 'shortlist', 'defer', 'reject'];
  function reviewChoices() {
    var out = {};
    selects.forEach(function (select) {
      if (validChoices.indexOf(select.value) !== -1) out[select.getAttribute('data-decision-id')] = select.value;
    });
    return out;
  }
  var answerFields = all('[data-answer-id]');
  function reviewAnswers() {
    var out = {};
    answerFields.forEach(function (field) {
      var value = field.value.replace(/^\s+|\s+$/g, '');
      if (value) out[field.getAttribute('data-answer-id')] = value.slice(0, 2000);
    });
    return out;
  }
  function reviewRecord() {
    return { schema: 'zone3.editorial-review.v2', saved_at: new Date().toISOString(), implementation: 'none; review only', choices: reviewChoices(), answers: reviewAnswers() };
  }
  if (selects.length || answerFields.length) {
    try {
      var stored = JSON.parse(localStorage.getItem(storageKey) || 'null');
      if (stored && (stored.schema === 'zone3.editorial-review.v2' || stored.schema === 'zone3.editorial-review.v1')) {
        var loaded = false;
        if (stored.choices) {
          selects.forEach(function (select) {
            var value = stored.choices[select.getAttribute('data-decision-id')];
            if (validChoices.indexOf(value) !== -1) select.value = value;
          });
          loaded = true;
        }
        if (stored.schema === 'zone3.editorial-review.v2' && stored.answers) {
          answerFields.forEach(function (field) {
            var value = stored.answers[field.getAttribute('data-answer-id')];
            if (typeof value === 'string') field.value = value;
          });
          loaded = true;
        }
        if (loaded) status.textContent = 'Loaded your saved review from this browser. No changes were implemented.';
      }
    } catch (error) { status.textContent = 'Browser storage is unavailable. You can still review and export without saving.'; }
    selects.forEach(function (select) { select.addEventListener('change', function () { status.textContent = 'Unsaved review choices. Nothing has been implemented.'; }); });
    answerFields.forEach(function (field) { field.addEventListener('input', function () { status.textContent = 'Unsaved answers. Nothing has been implemented.'; }); });
    document.querySelector('[data-save-review]').addEventListener('click', function () {
      try {
        localStorage.setItem(storageKey, JSON.stringify(reviewRecord()));
        status.textContent = 'Review saved in this browser only. No site or account changes were implemented.';
      } catch (error) { status.textContent = 'This browser could not save the review. Use Export to download your choices instead.'; }
    });
    document.querySelector('[data-reset-review]').addEventListener('click', function () {
      try { localStorage.removeItem(storageKey); } catch (error) { /* continue with in-memory reset */ }
      selects.forEach(function (select) { select.value = 'unreviewed'; });
      answerFields.forEach(function (field) { field.value = ''; });
      status.textContent = 'Review choices and answers cleared. Nothing was implemented.';
    });
    document.querySelector('[data-export-review]').addEventListener('click', function () {
      var data = JSON.stringify(reviewRecord(), null, 2) + '\n';
      var url = URL.createObjectURL(new Blob([data], { type: 'application/json' }));
      var link = document.createElement('a'); link.href = url; link.download = 'zone3-editorial-review.json';
      document.body.appendChild(link); link.click(); link.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
      status.textContent = 'Review exported. The download is not an implementation request.';
    });
  }
  // Copy the brief — whole, or one block at a time — without dragging the button labels into it.
  function plainText(element) {
    var clone = element.cloneNode(true);
    Array.prototype.forEach.call(clone.querySelectorAll('button'), function (b) { b.remove(); });
    return clone.textContent.replace(/[ \t]+/g, ' ').replace(/ ?\n ?/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  }
  var message = document.getElementById('p26-copy-status');
  function copyTo(target, label) {
    var text = plainText(target);
    if (!navigator.clipboard || !navigator.clipboard.writeText) { if (message) message.textContent = ' Clipboard is unavailable. Select the ' + label + ' text to copy it.'; return; }
    navigator.clipboard.writeText(text).then(function () {
      if (message) message.textContent = ' ' + (label === 'brief' ? 'Whole brief copied.' : 'Block copied.') + ' Nothing was published or changed.';
    }, function () { if (message) message.textContent = ' Copy was blocked. Select the ' + label + ' text to copy it.'; });
  }
  var whole = document.querySelector('[data-copy-prompt]');
  if (whole) whole.addEventListener('click', function () {
    var block = document.getElementById('p26-design-prompt');
    if (block) copyTo(block, 'brief');
  });
  all('[data-copy-from]').forEach(function (button) {
    button.addEventListener('click', function () {
      var block = document.getElementById(button.getAttribute('data-copy-from'));
      if (block) copyTo(block, 'block');
    });
  });
})();
