/* Zone3 outbound-click and page-event counter (build 38650305).
 * Privacy rules, enforced here and documented on measurement/index.html:
 *  - off unless window.Z3_MEASURE.enabled is true AND an endpoint is set;
 *  - nothing is sent when Global Privacy Control or Do Not Track is on;
 *  - no cookies, no storage, no visitor identifier;
 *  - the path is sent without query string or hash; link tokens are path segments only.
 * Events: page_view, outbound_click, guide_view, intent_view, flag_view.
 */
(function () {
  'use strict';
  var cfg = window.Z3_MEASURE || {};
  var EVENTS = ['page_view', 'outbound_click', 'guide_view', 'intent_view', 'flag_view'];

  function allowed() {
    if (!cfg.enabled || !cfg.endpoint) return false;
    if (navigator.globalPrivacyControl === true) return false;
    if (navigator.doNotTrack === '1' || window.doNotTrack === '1') return false;
    return true;
  }

  function send(name, extra) {
    if (!allowed() || EVENTS.indexOf(name) < 0) return;
    var body = { v: 1, e: name, p: location.pathname, h: '' };
    if (extra) {
      for (var k in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, k)) body[k] = extra[k];
      }
    }
    var data = JSON.stringify(body);
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(cfg.endpoint, new Blob([data], { type: 'text/plain' }));
      } else {
        fetch(cfg.endpoint, { method: 'POST', body: data, keepalive: true, mode: 'no-cors' });
      }
    } catch (err) {
      /* counting must never break the page */
    }
  }

  function linkParts(href) {
    try {
      var u = new URL(href, location.href);
      var seg = u.pathname.split('/').filter(Boolean).pop() || '';
      return { h: u.hostname, t: /^[A-Za-z0-9]{4,20}$/.test(seg) ? seg : '' };
    } catch (err) {
      return { h: '', t: '' };
    }
  }

  function pageEvents() {
    var path = location.pathname;
    send('page_view');
    if (/\/guides\/[^\/]+\.html$/.test(path) && !/\/index\.html$/.test(path)) send('guide_view');
    if (/\/intent-record\/(index\.html)?$/.test(path)) send('intent_view');
    if (/\/publication-pass\.html$|\/flagged\.html$|\/flagged\/(index\.html)?$/.test(path)) send('flag_view');
  }

  document.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!t || !t.closest) return;
    var a = t.closest('a[rel~="sponsored"]');
    if (!a || !a.href) return;
    send('outbound_click', linkParts(a.href));
  }, true);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pageEvents);
  } else {
    pageEvents();
  }
})();
