/*
 * Gordon Smith Gallery: header navigation and sideways rows (DESIGN.md §6.1, DS-11).
 * Theme copy: theme/assets/gs-nav.js, loaded with `defer`.
 *
 * The header works without this file. The Menu drawer and every dropdown are <details>
 * elements (snippets/gs-header.liquid, gs-nav.liquid): a click, tap, Enter or Space on a
 * section's button opens its dropdown, and dropdowns in one menu share a `name`, so opening
 * one closes the others. Nothing opens on hover. This file adds what <details> can't do alone:
 *
 *   - Escape closes the open dropdown and returns focus to its button; pressed again (or with
 *     no dropdown open) it closes the Menu drawer and returns focus to the Menu button.
 *   - A click outside the header closes any open dropdown and the drawer.
 *   - Desktop bar (1200px and up): focus leaving a dropdown closes it.
 *   - Focus leaving the Menu drawer closes it.
 *   - Choosing a link in the drawer closes the drawer (matters for links within the page).
 *   - Crossing the 1200px breakpoint closes everything.
 *   - One-open-at-a-time for browsers without <details name> support.
 *   - A card in a sideways row (.gs-rail) that gets keyboard focus scrolls into view whole.
 *
 * Markup contract:
 *   <header class="gs-header" data-gs-header>
 *     <details class="gs-drawer"><summary class="gs-header__menu-toggle">Menu</summary>
 *       <div class="gs-drawer__panel"> nav (variant drawer) + utility </div></details>
 *     <div class="gs-header__bar"> utility + nav (variant bar) </div>
 *   Each dropdown: <details class="gs-nav__details" name="gs-nav-bar|gs-nav-drawer">
 *                    <summary class="gs-nav__trigger">Exhibitions</summary>
 *                    <ul class="gs-nav__panel">…</ul></details>
 */
(function () {
  "use strict";

  var DESKTOP = window.matchMedia("(min-width: 1200px)"); /* keep in step with components.css */
  var NATIVE_NAME = "name" in HTMLDetailsElement.prototype;

  function summaryOf(details) {
    return details.querySelector("summary");
  }

  function close(details, returnFocus) {
    if (!details || !details.open) return;
    details.open = false;
    if (returnFocus) summaryOf(details).focus();
  }

  function initHeader(header) {
    var drawer = header.querySelector(".gs-drawer");
    var dropdowns = Array.prototype.slice.call(header.querySelectorAll(".gs-nav__details"));

    function closeAll() {
      dropdowns.forEach(function (d) { close(d); });
      close(drawer);
    }

    dropdowns.forEach(function (details) {
      if (!NATIVE_NAME) {
        details.addEventListener("toggle", function () {
          if (!details.open) return;
          var group = details.getAttribute("name");
          dropdowns.forEach(function (other) {
            if (other !== details && other.getAttribute("name") === group) close(other);
          });
        });
      }

      details.addEventListener("focusout", function (event) {
        if (!DESKTOP.matches || !details.closest(".gs-header__bar")) return;
        if (event.relatedTarget && details.contains(event.relatedTarget)) return;
        close(details);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape" && event.key !== "Esc") return;
      var target = event.target instanceof Element ? event.target : null;
      var openDetails = target && target.closest("details[open]");
      if (openDetails && header.contains(openDetails)) {
        close(openDetails, true);
        return;
      }
      closeAll();
    });

    document.addEventListener("click", function (event) {
      if (!header.contains(event.target)) closeAll();
    });

    if (drawer) {
      drawer.addEventListener("click", function (event) {
        if (event.target instanceof Element && event.target.closest(".gs-drawer__panel a[href]")) close(drawer);
      });

      drawer.addEventListener("focusout", function (event) {
        var next = event.relatedTarget;
        if (DESKTOP.matches || (next && drawer.contains(next))) return;
        if (!next) {
          /* A click or tap (focus stays on the page body or in the drawer; the outside-click rule
             handles the rest), or focus moving into an embedded video's frame, which reports no target. */
          setTimeout(function () {
            var now = document.activeElement;
            if (now && now !== document.body && !drawer.contains(now)) close(drawer);
          }, 0);
          return;
        }
        close(drawer);
      });
    }

    if (DESKTOP.addEventListener) DESKTOP.addEventListener("change", closeAll);
    else if (DESKTOP.addListener) DESKTOP.addListener(closeAll);
  }

  function init() {
    document.querySelectorAll("[data-gs-header]").forEach(initHeader);

    /* A sideways row on phones (.gs-rail): a card reached with the keyboard scrolls into view whole.
       Keyboard focus only: scrolling under a click or tap moves the card before the click lands. */
    document.addEventListener("focusin", function (event) {
      var target = event.target, item;
      if (!(target instanceof Element)) return;
      try { if (!target.matches(":focus-visible")) return; } catch (err) { return; }
      item = target.closest(".gs-rail > li");
      if (item && getComputedStyle(item.parentNode).overflowX !== "visible") {
        item.scrollIntoView({ block: "nearest", inline: "start" });
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
