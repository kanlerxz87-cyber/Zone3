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
