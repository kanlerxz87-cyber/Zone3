/* Zone3 measurement layer — the five defined events, privacy-preserving.
 *
 * Schema of record: data/analytics.json (0C4-T4, session 0c4c4cb6, 2026-11-17).
 * Reference endpoint: tools/analytics_collector.py.
 *
 * What this file does:
 *   page_view            once per page load
 *   guide_view           once, when an article/guide scrolls past halfway
 *   product_click        on any outbound Amazon product link
 *   special_link_click   on a product link whose href carries tag=
 *   nav_click            on internal navigation links
 *
 * What it deliberately does NOT do: no cookies, no storage, no identifiers,
 * no query strings, no full referrer paths. Do Not Track / Global Privacy
 * Control / Save-Data switch it off completely. While
 * window.ZONE3_ANALYTICS_ENDPOINT is null (the shipped state) nothing is
 * sent at all — the site works exactly as before, minus measurement.
 */
(function () {
  "use strict";

  var ENDPOINT = (typeof window !== "undefined" && window.ZONE3_ANALYTICS_ENDPOINT) || null;
  var SCHEMA = ["page_view", "guide_view", "product_click", "special_link_click", "nav_click"];

  function disabled() {
    try {
      if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return true;
      if (navigator.globalPrivacyControl === true) return true;
      if (navigator.connection && navigator.connection.saveData === true) return true;
    } catch (err) { /* private mode oddities: fail closed */ }
    return false;
  }

  function pathOf(url) {
    try {
      var u = new URL(url, window.location.href);
      return u.pathname || "/"; // query and fragment stripped by construction
    } catch (err) {
      return null;
    }
  }

  function refHost() {
    try {
      return document.referrer ? new URL(document.referrer).hostname : "";
    } catch (err) {
      return "";
    }
  }

  function send(event, extra) {
    if (!ENDPOINT || disabled() || SCHEMA.indexOf(event) === -1) return;
    var payload = {
      e: event,
      p: pathOf(window.location.href) || "/",
      r: refHost(),
      t: new Date().toISOString()
    };
    if (extra) {
      if (extra.p) payload.p = extra.p; // target path for nav_click
      if (extra.r) payload.r = extra.r; // destination host for clicks
    }
    var body = JSON.stringify(payload);
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "application/json" }));
      } else {
        fetch(ENDPOINT, { method: "POST", body: body, headers: { "Content-Type": "application/json" }, keepalive: true, credentials: "omit", mode: "cors" });
      }
    } catch (err) { /* measurement must never break the page */ }
  }

  function isAmazonProduct(anchor) {
    var href = anchor.getAttribute("href") || "";
    if (href.indexOf("https://link.amazon/") === 0) return true;
    try {
      var u = new URL(href, window.location.href);
      if (u.hostname !== "amazon.com" && u.hostname !== "www.amazon.com") return false;
      return u.pathname.indexOf("/dp/") !== -1 || u.pathname.indexOf("/gp/product/") !== -1;
    } catch (err) {
      return false;
    }
  }

  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  onReady(function () {
    send("page_view");

    // product clicks: every outbound Amazon product link, sponsored or not
    document.addEventListener("click", function (ev) {
      var a = ev.target && ev.target.closest ? ev.target.closest("a") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (isAmazonProduct(a)) {
        send(href.indexOf("tag=") !== -1 ? "special_link_click" : "product_click", {
          r: (function () { try { return new URL(href, window.location.href).hostname; } catch (e) { return ""; } })()
        });
        return;
      }
      if (href && href.charAt(0) !== "#" && href.indexOf("mailto:") !== 0) {
        var internal = a.closest && (a.closest("nav") || a.closest(".acts") || a.closest(".topbar"));
        if (internal) {
          send("nav_click", { p: pathOf(a.href) || href });
        }
      }
    }, { capture: true });

    // guide_view: halfway into the main content of an article/guide page
    var isArticle = /\/(articles|guides|read)\//.test(window.location.pathname) ||
                    document.querySelector("article, .guide, .article") !== null;
    if (isArticle && "IntersectionObserver" in window) {
      var target = document.querySelector("main, article, .guide, .article") || document.body;
      var seen = false;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!seen && entry.isIntersecting && entry.intersectionRatio >= 0.5) {
            seen = true;
            send("guide_view");
            io.disconnect();
          }
        });
      }, { threshold: [0.5] });
      io.observe(target);
    }
  });
})();
