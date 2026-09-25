/*
 * Gordon Smith Gallery: form states (DESIGN.md §6.9, §6.12).
 * Theme copy: theme/assets/gs-forms.js, loaded with `defer`.
 *
 * Forms work without this file: they post normally, the browser checks email fields, and Shopify's
 * reply shows the error or done state. This file adds, for forms marked data-gs-form:
 *
 *   - An empty or malformed email address shows the design system's error under the field
 *     (aria-invalid, linked with aria-describedby, focus moved to the field) instead of the
 *     browser's bubble.
 *   - While sending, the submit button says what's happening (data-gs-busy-label, e.g.
 *     "Signing up"), gets aria-busy, and repeat submits are ignored.
 *
 * Markup contract:
 *   <form data-gs-form>
 *     <input type="email" id="X" aria-describedby="X-error">
 *     <p class="gs-field__error" id="X-error" hidden>Enter an email address like name@example.com.</p>
 *     <button type="submit" class="gs-button" data-gs-busy-label="Signing up">Sign up</button>
 *   </form>
 */
(function () {
  "use strict";

  function errorFor(input) {
    var ids = (input.getAttribute("aria-describedby") || "").split(/\s+/);
    for (var i = 0; i < ids.length; i++) {
      var el = ids[i] && document.getElementById(ids[i]);
      if (el && el.classList.contains("gs-field__error")) return el;
    }
    return null;
  }

  function setInvalid(input, invalid) {
    var message = errorFor(input);
    if (invalid) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
    if (message) message.hidden = !invalid;
  }

  function initForm(form) {
    form.noValidate = true;
    var emails = Array.prototype.slice.call(form.querySelectorAll('input[type="email"]'));

    emails.forEach(function (input) {
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
      emails.forEach(function (input) {
        var bad = !input.value.trim() || !input.checkValidity();
        setInvalid(input, bad);
        if (bad && !firstBad) firstBad = input;
      });
      if (firstBad) {
        event.preventDefault();
        firstBad.focus();
        return;
      }
      var button = form.querySelector("[data-gs-busy-label]");
      form.setAttribute("aria-busy", "true");
      if (button) {
        button.setAttribute("aria-busy", "true");
        button.textContent = button.getAttribute("data-gs-busy-label");
      }
    });
  }

  /* Coming back with the Back button can restore a page from memory with the button still
     saying "Signing up". Put it back. */
  function reset(form) {
    form.removeAttribute("aria-busy");
    var button = form.querySelector("[data-gs-busy-label]");
    if (button && button.hasAttribute("data-gs-label")) {
      button.removeAttribute("aria-busy");
      button.textContent = button.getAttribute("data-gs-label");
    }
  }

  function init() {
    document.querySelectorAll("form[data-gs-form]").forEach(function (form) {
      var button = form.querySelector("[data-gs-busy-label]");
      if (button) button.setAttribute("data-gs-label", button.textContent.trim());
      initForm(form);
    });
    window.addEventListener("pageshow", function (event) {
      if (event.persisted) document.querySelectorAll("form[data-gs-form]").forEach(reset);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
