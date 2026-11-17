(function(){
  var KEY = 'i2-decisions-v1';
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e) { state = {}; }
  var proposals = Array.prototype.slice.call(document.querySelectorAll('.prop[id^="D-"]'));
  var exportBox = document.getElementById('exportBox');
  var countEl = document.getElementById('count');

  function save(){ try { localStorage.setItem(KEY, JSON.stringify(state)); } catch(e){} }
  function decided(){
    return proposals.filter(function(p){ return state[p.id] && state[p.id].decision; }).length;
  }
  function refreshCount(){
    if (!countEl) return;
    countEl.textContent = decided() + ' of ' + proposals.length + ' decided';
  }
  function refreshOutputs(){
    proposals.forEach(function(p){
      var out = p.querySelector('[data-out]');
      var s = state[p.id];
      if (!out) return;
      if (s && s.decision) {
        out.textContent = 'Recorded: ' + s.decision + (s.note ? ' — ' + s.note : '');
        out.style.color = '#0b6b53';
      } else {
        out.textContent = 'No decision recorded yet';
        out.style.color = '';
      }
    });
    refreshCount();
  }

  proposals.forEach(function(p){
    var radios = p.querySelectorAll('input[type=radio]');
    var note = p.querySelector('[data-note]');
    var s = state[p.id] || {};
    if (s.decision) {
      radios.forEach(function(r){ if (r.value === s.decision) r.checked = true; });
    }
    if (s.note && note) note.value = s.note;
    radios.forEach(function(r){
      r.addEventListener('change', function(){
        state[p.id] = state[p.id] || {};
        state[p.id].decision = r.value;
        state[p.id].title = p.querySelector('h3').textContent;
        if (note) state[p.id].note = note.value.trim();
        save(); refreshOutputs();
      });
    });
    if (note) note.addEventListener('input', function(){
      state[p.id] = state[p.id] || {};
      state[p.id].note = note.value.trim();
      state[p.id].title = p.querySelector('h3').textContent;
      save(); refreshOutputs();
    });
  });

  var btn = document.getElementById('exportBtn');
  if (btn && exportBox) btn.addEventListener('click', function(){
    var lines = ['Decision record — ' + new Date().toISOString().slice(0,10), ''];
    proposals.forEach(function(p){
      var s = state[p.id];
      lines.push(p.id + ' — ' + (p.querySelector('h3').textContent || '') );
      lines.push('  Decision: ' + (s && s.decision ? s.decision : 'not decided'));
      if (s && s.note) lines.push('  Reason: ' + s.note);
      lines.push('');
    });
    var open = proposals.length - decided();
    lines.push(open ? open + ' proposal(s) still undecided.' : 'All proposals decided.');
    exportBox.value = lines.join('\n');
    exportBox.select();
    exportBox.focus();
  });

  var print = document.getElementById('printBtn');
  if (print) print.addEventListener('click', function(){ window.print(); });

  refreshOutputs();
})();

/* ---- First-party event ledger (session ded63349, 2026-11-17; proposal D-16) ----
   Five defined events, recorded on this device only: no cookies, no third-party
   requests, no identifiers, no referrer storage — just event name, UTC timestamp,
   page path and (for product clicks) which product card. Participation Requirements
   6(s) bans artificial clicks or sessions: this ledger counts real clicks made by a
   real visitor on this site's own pages, and never touches Amazon sessions. */
(function(){
  var KEY = 'z3-events-v1', MAX = 500;
  var EVENTS = { page_view:1, outbound_product_click:1, comparison_open:1, guide_read_through:1, decision_open:1 };
  function load(){ try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch(e){ return []; } }
  function save(a){ try { localStorage.setItem(KEY, JSON.stringify(a.slice(-MAX))); } catch(e){} }
  function rec(name, data){
    if (!EVENTS[name]) return;
    var a = load();
    a.push({ t: new Date().toISOString(), e: name,
             p: location.pathname.replace(/^\/Zone3/, ''),
             r: (data && data.ref) ? data.ref : null });
    save(a);
    try { document.dispatchEvent(new CustomEvent('z3-event', { detail: { name: name } })); } catch(e){}
  }
  rec('page_view');
  document.addEventListener('click', function(ev){
    var t = ev.target;
    var a = t && t.closest ? t.closest('a') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('/dp/') > -1 || href.indexOf('link.amazon') > -1) {
      rec('outbound_product_click', { ref: a.getAttribute('data-ref') || '' });
    } else if (href.indexOf('compare') > -1 || (a.textContent || '').toLowerCase().indexOf('compare') > -1
               || href.indexOf('products.html') > -1) {
      rec('comparison_open');
    } else if (href.indexOf('decisions.html') > -1 || href.indexOf('answers.html') > -1) {
      rec('decision_open');
    }
  }, true);
  if (location.pathname.indexOf('/guides/') > -1) {
    var readFired = false;
    window.addEventListener('scroll', function(){
      if (readFired) return;
      var d = document.documentElement;
      var total = (d.scrollHeight || 1) - (d.clientHeight || 1);
      var progress = (d.scrollTop || document.body.scrollTop || 0) / (total || 1);
      if (progress > 0.92) { readFired = true; rec('guide_read_through'); }
    }, { passive: true });
  }
  window.z3Ledger = {
    events: Object.keys(EVENTS),
    all: load,
    record: rec,
    clear: function(){ try { localStorage.removeItem(KEY); } catch(e){} },
    csv: function(){
      var rows = ['timestamp,event,path,product'];
      load().forEach(function(x){
        var cells = [x.t, x.e, x.p, x.r || ''];
        rows.push(cells.map(function(v){ return '"' + String(v).replace(/"/g, '""') + '"'; }).join(','));
      });
      return rows.join('\n');
    }
  };
})();
