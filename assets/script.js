/* Zone3 — shared site script */
/* Client-side affiliate click tracking (localStorage). Production: server-side or Amazon reporting API. */

(function(){
  function recordClick(link){
    var href = link.getAttribute('href') || '';
    var productId = null;
    if (/link\.amazon\/B04G1MEwY/.test(href)) productId = 1;
    if (/link\.amazon\/B02NbDxp3/.test(href)) productId = 2;
    if (/link\.amazon\/B00hJ57DV/.test(href)) productId = 3;
    if (/amazon\.com\/dp\/B0CDY277D3/.test(href)) productId = 1;
    if (/amazon\.com\/dp\/B09B7SB46R/.test(href)) productId = 2;
    if (/amazon\.com\/dp\/B08DKYBTPH/.test(href)) productId = 3;
    if (productId === null) return;
    var key = 'zone3:clicks:' + productId;
    var current = parseInt(localStorage.getItem(key) || '0', 10);
    localStorage.setItem(key, String(current + 1));
  }

  var links = document.querySelectorAll('a');
  for (var i = 0; i < links.length; i++) {
    (function(l){
      l.addEventListener('click', function(){ recordClick(l); });
    })(links[i]);
  }

  // Highlight active nav link based on current path
  var path = window.location.pathname.split('/').pop() || 'index.html';
  var navLinks = document.querySelectorAll('.navLinks a');
  for (var j = 0; j < navLinks.length; j++) {
    var href = navLinks[j].getAttribute('href');
    if (href && href.split('/').pop() === path) {
      navLinks[j].classList.add('active');
    }
  }
})();
