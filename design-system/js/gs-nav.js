/*
 * Gordon Smith Gallery: header navigation and sideways rows (DESIGN.md §6.1, DS-11).
 * Theme copy: theme/assets/gs-nav.js, loaded with `defer`.
 *
 * The header works without this file. The Menu drawer and every dropdown are <details>
 * elements (snippets/gs-header.liquid, gs-nav.liquid): a click, tap, Enter or Space on a
 * section's button opens its dropdown, and the bar's dropdowns share a `name`, so opening
 * one closes the others; the drawer's sections open independently (DS-104). Nothing opens on hover. This file adds what <details> can't do alone:
 *
 *   - Escape closes the open dropdown and returns focus to its button; pressed again (or with
 *     no dropdown open) it closes the Menu drawer and returns focus to the Menu button.
 *   - A click outside the header closes any open dropdown and the drawer; a click elsewhere in
 *     the header closes the bar's open dropdown. A click inside a dropdown never closes it.
 *   - Desktop bar (1200px and up): focus moving out of a dropdown to another element closes it.
 *   - Focus leaving the Menu drawer closes it.
 *   - Choosing a link in the drawer closes the drawer (matters for links within the page).
 *   - Crossing the 1200px breakpoint closes everything.
 *   - One-open-at-a-time on the bar for browsers without <details name> support.
 *   - Below 990px the header stays at the top of the screen (DS-190): once the page scrolls
 *     under it, data-stuck on the header draws a hairline along its edge.
 *   - A card in a sideways row (.gs-rail) that gets keyboard focus scrolls into view whole.
 *
 * Markup contract:
 *   <header class="gs-header" data-gs-header>
 *     <details class="gs-drawer"><summary class="gs-header__menu-toggle">Menu</summary>
 *       <div class="gs-drawer__panel"> nav (variant drawer) + utility </div></details>
 *     <div class="gs-header__bar"> utility + nav (variant bar) </div>
 *   Each dropdown: <details class="gs-nav__details" name="gs-nav-bar"> (no name in the drawer)
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
          if (!group) return; /* the drawer's sections have no name: they open independently */
          dropdowns.forEach(function (other) {
            if (other !== details && other.getAttribute("name") === group) close(other);
          });
        });
      }

      /* Focus moving to somewhere else on the page (Tab, Shift+Tab) closes a bar dropdown. A click on
         a spot that can't take focus (a heading, the space between links) reports no target: the
         dropdown stays open, and the click rule below closes it when the spot is outside. Closing
         it mid-click crashed Chrome 154 ("Aw, Snap!"). */
      details.addEventListener("focusout", function (event) {
        if (!DESKTOP.matches || !details.closest(".gs-header__bar")) return;
        if (!event.relatedTarget || details.contains(event.relatedTarget)) return;
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
      if (!header.contains(event.target)) {
        closeAll();
        return;
      }
      /* A click elsewhere in the header (the utility row, the gap between sections) closes the bar's
         open dropdown; a click inside it leaves it open. */
      dropdowns.forEach(function (d) {
        if (d.closest(".gs-header__bar") && !d.contains(event.target)) close(d);
      });
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

    /* The header only sticks below 990px (components.css), and only there does the hairline show. */
    function markStuck() { header.toggleAttribute("data-stuck", window.scrollY > 0); }
    window.addEventListener("scroll", markStuck, { passive: true });
    markStuck();

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
