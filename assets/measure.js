/* Zone3's ONE active five-event counter.
 * No cookies/storage/visitor IDs; no query strings, fragments, referrers or credentials.
 * Production is off until configured. Preview uses a real same-origin /collect endpoint.
 * A click is not an order, session, unique person, or conversion.
 */
(function () {
  'use strict';
  if (window.__z3MeasureInitialized) return;
  window.__z3MeasureInitialized = true;
  var cfg = window.Z3_MEASURE || {};
  var EVENTS = ['page_view', 'outbound_click', 'guide_view', 'intent_view', 'flag_view'];
  var HOSTS = ['link.amazon', 'amazon.com', 'www.amazon.com'];

  function endpoint() {
    if (cfg.enabled !== true || typeof cfg.endpoint !== 'string' || !cfg.endpoint) return '';
    try {
      var current = new URL(location.href);
      var target = new URL(cfg.endpoint, current);
      var localPreview = target.origin === current.origin && /^(localhost|127\.0\.0\.1)$/.test(current.hostname);
      if (target.protocol !== 'https:' && !(localPreview && target.protocol === 'http:')) return '';
      if (target.username || target.password || target.search || target.hash || !/\/collect$/.test(target.pathname)) return '';
      return target.href;
    } catch (error) { return ''; }
  }

  function allowed() {
    if (!endpoint() || typeof fetch !== 'function') return false;
    if (navigator.globalPrivacyControl === true) return false;
    if (navigator.doNotTrack === '1' || window.doNotTrack === '1') return false;
    if (navigator.connection && navigator.connection.saveData === true) return false;
    return true;
  }

  function send(name, link) {
    if (!allowed() || EVENTS.indexOf(name) < 0) return;
    var path = location.pathname;
    if (typeof path !== 'string' || !/^\/[A-Za-z0-9/_.-]{0,199}$/.test(path) || path.indexOf('..') !== -1 || path.indexOf('//') !== -1) return;
    var body = { v: 1, e: name, p: path, h: '' };
    if (name === 'outbound_click') {
      if (!link) return;
      body.h = link.h; body.t = link.t;
    }
    try {
      // Unlike sendBeacon, fetch lets us explicitly omit credentials and the Referer.
      var request = fetch(endpoint(), {
        method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'text/plain' },
        credentials: 'omit', referrerPolicy: 'no-referrer', keepalive: true, mode: 'cors',
        cache: 'no-store', redirect: 'error'
      });
      if (request && request.catch) request.catch(function () { /* measurement never breaks navigation */ });
    } catch (error) { /* failure is not a successful count; leave the page usable */ }
  }

  function linkParts(href) {
    try {
      var url = new URL(href, location.href);
      if (url.protocol !== 'https:' || HOSTS.indexOf(url.hostname) < 0) return null;
      var match = url.hostname === 'link.amazon' ? url.pathname.match(/^\/([A-Za-z0-9]{9})\/?$/) : url.pathname.match(/\/(?:dp|gp\/product)\/([A-Za-z0-9]{9,10})(?:\/|$)/);
      return match ? { h: url.hostname, t: match[1] } : null;
    } catch (error) { return null; }
  }

  function pageEvents() {
    var path = location.pathname;
    send('page_view');
    if (/\/(?:guides|articles|read)\/[^/]+\.html$/.test(path) && !/\/index\.html$/.test(path)) send('guide_view');
    if (/\/intent-record\/(?:index\.html)?$|\/intent-record\.html$/.test(path)) send('intent_view');
    if (/\/(?:publication-pass|flagged)\.html$|\/flagged\/(?:index\.html)?$/.test(path)) send('flag_view');
  }

  function outbound(event) {
    var target = event.target;
    if (!target || !target.closest) return;
    var anchor = target.closest('a[rel~="sponsored"]');
    if (anchor && anchor.href) send('outbound_click', linkParts(anchor.href));
  }
  document.addEventListener('click', outbound, true);
  document.addEventListener('auxclick', function (event) { if (event.button === 1) outbound(event); }, true);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pageEvents, { once: true });
  else pageEvents();
})();
