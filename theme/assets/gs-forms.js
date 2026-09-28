/*
 * Gordon Smith Gallery: form states (DESIGN.md §6.9, §6.12).
 * Theme copy: theme/assets/gs-forms.js, loaded with `defer`.
 *
 * Forms work without this file: they post normally, the browser checks required and email fields,
 * and Shopify's reply shows the error or done state. This file adds, for forms marked data-gs-form:
 *
 *   - An empty required field, or a malformed email address, shows the design system's error under
 *     the field instead of the browser's bubble: aria-invalid, the error linked with
 *     aria-describedby only while it shows, focus moved to the first field in error. Nothing posts,
 *     and no other submit listener (such as Shopify's spam check) runs.
 *   - While sending, the submit button says what's happening (data-gs-busy-label, e.g.
 *     "Signing up"), keeps its width, gets aria-busy, and repeat submits are ignored. Shopify's
 *     spam check can hold the post; if the page hasn't left after 10 seconds, the button returns
 *     to its label.
 *   - After a post, focus moves to the first field in error, or else to the done line
 *     (.gs-form-status, tabindex="-1"), so it's read out. Shopify's reply page opens at the
 *     form's #id, where autofocus doesn't fire.
 *
 * Markup contract (the error's id is always the field's id plus "-error"):
 *   <form data-gs-form>
 *     <input type="email" id="X" required>
 *     <p class="gs-field__error" id="X-error" hidden>Enter an email address like name@example.com.</p>
 *     <p class="gs-form-status" role="status" tabindex="-1">Done wording (only after a post)</p>
 *     <button type="submit" class="gs-button" data-gs-busy-label="Signing up">Sign up</button>
 *   </form>
 *   The server's reply may render an error shown: aria-invalid="true" on the field and X-error in
 *   its aria-describedby. At rest the hidden error is not referenced.
 */
(function () {
  "use strict";

  var RESET_AFTER = 10000; /* ms: a held post (spam check closed) gives the button back */

  function errorFor(input) {
    return input.id ? document.getElementById(input.id + "-error") : null;
  }

  function setDescribedBy(input, id, on) {
    var ids = (input.getAttribute("aria-describedby") || "").split(/\s+/).filter(function (x) {
      return x && x !== id;
    });
    if (on) ids.unshift(id);
    if (ids.length) input.setAttribute("aria-describedby", ids.join(" "));
    else input.removeAttribute("aria-describedby");
  }

  function setInvalid(input, invalid) {
    var message = errorFor(input);
    if (invalid) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
    if (message) {
      message.hidden = !invalid;
      setDescribedBy(input, message.id, invalid);
    }
  }

  function initForm(form) {
    form.noValidate = true;
    var fields = Array.prototype.slice.call(form.querySelectorAll('input[type="email"], [required]'));

    fields.forEach(function (input) {
      input.addEventListener("input", function () {
        if (input.getAttribute("aria-invalid") === "true" && input.checkValidity() && input.value.trim()) {
          setInvalid(input, false);
        }
      });
    });

    form.addEventListener("submit", function (event) {
      if (form.getAttribute("aria-busy") === "true") {
        event.preventDefault();
        return;
      }
      var firstBad = null;
      fields.forEach(function (input) {
        var bad = !input.value.trim() || !input.checkValidity();
        setInvalid(input, bad);
        if (bad && !firstBad) firstBad = input;
      });
      if (firstBad) {
        event.preventDefault();
        event.stopImmediatePropagation();
        firstBad.focus();
        return;
      }
      var button = form.querySelector("[data-gs-busy-label]");
      form.setAttribute("aria-busy", "true");
      if (button) {
        button.style.minWidth = button.getBoundingClientRect().width + "px";
        button.setAttribute("aria-busy", "true");
        button.textContent = button.getAttribute("data-gs-busy-label");
      }
      var left = false;
      window.addEventListener("beforeunload", function () { left = true; }, { once: true });
      setTimeout(function () { if (!left) reset(form); }, RESET_AFTER);
    });
  }

  /* Puts the button back: after a held post, or when the Back button restores a page from memory
     with the button still saying "Signing up". */
  function reset(form) {
    form.removeAttribute("aria-busy");
    var button = form.querySelector("[data-gs-busy-label]");
    if (button && button.hasAttribute("data-gs-label")) {
      button.removeAttribute("aria-busy");
      button.textContent = button.getAttribute("data-gs-label");
      button.style.minWidth = "";
    }
  }

  function init() {
    document.querySelectorAll("form[data-gs-form]").forEach(function (form) {
      var button = form.querySelector("[data-gs-busy-label]");
      if (button) button.setAttribute("data-gs-label", button.textContent.trim());
      initForm(form);
      var target = form.querySelector('[aria-invalid="true"]') || form.querySelector(".gs-form-status");
      if (target) target.focus();
    });
    window.addEventListener("pageshow", function (event) {
      if (event.persisted) document.querySelectorAll("form[data-gs-form]").forEach(reset);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
