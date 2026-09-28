/*
 * Gordon Smith Gallery: the larger view of an image, a lightbox (DESIGN.md §6.8, DS-139).
 * Theme copy: theme/assets/gs-lightbox.js, loaded with `defer`.
 *
 * An image that opens larger is a link to its full-size file ([data-gs-lightbox-item], written by
 * snippets/gs-media.liquid with enlarge), inside a group ([data-gs-lightbox]): a work's views, or
 * an exhibition's installation views. Without this script the link opens the file. With it, a
 * click opens a full-screen dialog on the mat: the whole image, never cropped, the group's caption
 * (its <template data-gs-lightbox-caption>), "2 of 6", Close, and Previous and Next when the group
 * has more than one. Escape, Close and the Back button close it; the arrow keys and a swipe move
 * through the group, round from the last to the first. The dialog is snippets/gs-lightbox.liquid,
 * a <template> carrying the wording from the theme's locale file.
 *
 * The thumbnail is already loaded, so it shows at once, and the sharper size the screen needs
 * replaces it when it has arrived: never an empty stage, never a spinner (DESIGN.md §5.4).
 */
(() => {
  const template = document.querySelector('template[data-gs-lightbox-template]');
  if (!template || !document.querySelector('[data-gs-lightbox-item]')) return;
  if (typeof HTMLDialogElement !== 'function') return; // An old browser keeps the link to the file.

  let dialog;
  let img;
  let count;
  let caption;
  let nav;
  let items = [];
  let index = 0;
  let opener = null;

  const show = (i) => {
    index = (i + items.length) % items.length;
    const link = items[index];
    const thumb = link.querySelector('img');
    img.removeAttribute('srcset');
    img.removeAttribute('sizes');
    img.src = thumb ? thumb.currentSrc || thumb.src : link.href;
    img.alt = thumb ? thumb.alt : '';
    if (thumb && thumb.srcset) {
      const sharp = new Image();
      sharp.sizes = '100vw';
      sharp.srcset = thumb.srcset;
      const wanted = link;
      sharp.decode().then(() => {
        if (items[index] !== wanted || !dialog.open) return;
        img.sizes = '100vw';
        img.srcset = thumb.srcset;
      }).catch(() => {});
    }
    count.textContent = count.dataset.text
      .replace('{n}', String(index + 1))
      .replace('{t}', String(items.length));
  };

  const build = () => {
    dialog = template.content.firstElementChild.cloneNode(true);
    img = document.createElement('img');
    img.className = 'gs-lightbox__img';
    img.decoding = 'async';
    dialog.querySelector('.gs-lightbox__stage').append(img);
    count = dialog.querySelector('.gs-lightbox__count');
    caption = dialog.querySelector('.gs-lightbox__caption');
    nav = dialog.querySelector('.gs-lightbox__nav');
    document.body.append(dialog);

    dialog.addEventListener('click', (event) => {
      const button = event.target.closest('[data-gs-lightbox-action]');
      if (!button) return;
      const action = button.dataset.gsLightboxAction;
      if (action === 'close') dialog.close();
      else show(index + (action === 'next' ? 1 : -1));
    });

    dialog.addEventListener('keydown', (event) => {
      if (items.length < 2 || event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.key === 'ArrowRight') {
        event.preventDefault();
        show(index + 1);
      } else if (event.key === 'ArrowLeft') {
        event.preventDefault();
        show(index - 1);
      }
    });

    // A swipe across the image moves through the group. Not while the page is pinch-zoomed, when
    // the same gesture moves around the enlarged image instead.
    let start = null;
    const stage = dialog.querySelector('.gs-lightbox__stage');
    stage.addEventListener('touchstart', (event) => {
      start = event.touches.length === 1
        ? { x: event.touches[0].clientX, y: event.touches[0].clientY }
        : null;
    }, { passive: true });
    stage.addEventListener('touchend', (event) => {
      if (!start || event.changedTouches.length !== 1 || items.length < 2) return;
      const dx = event.changedTouches[0].clientX - start.x;
      const dy = event.changedTouches[0].clientY - start.y;
      start = null;
      const zoomed = window.visualViewport && window.visualViewport.scale > 1.01;
      if (!zoomed && Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        show(index + (dx < 0 ? 1 : -1));
      }
    }, { passive: true });

    dialog.addEventListener('close', () => {
      img.removeAttribute('srcset');
      img.removeAttribute('src');
      // Closed by Close or Escape: take back the history entry opening added.
      if (history.state && history.state.gsLightbox) history.back();
      // Safari doesn't focus a link on click, so the dialog can't return focus to it by itself.
      if (opener && opener.isConnected) opener.focus({ preventScroll: true });
      opener = null;
    });

    // On a phone, Back closes the larger view instead of leaving the page.
    window.addEventListener('popstate', () => {
      if (dialog.open) dialog.close();
    });
  };

  const open = (link) => {
    if (!dialog) build();
    const group = link.closest('[data-gs-lightbox]');
    items = group ? [...group.querySelectorAll('[data-gs-lightbox-item]')] : [link];
    opener = link;
    const words = group && group.querySelector('template[data-gs-lightbox-caption]');
    caption.replaceChildren(...(words ? [words.content.cloneNode(true)] : []));
    const many = items.length > 1;
    count.hidden = !many;
    nav.hidden = !many;
    show(Math.max(0, items.indexOf(link)));
    dialog.showModal();
    history.pushState({ gsLightbox: true }, '');
  };

  document.addEventListener('click', (event) => {
    const link = event.target.closest('[data-gs-lightbox-item]');
    if (!link || event.defaultPrevented) return;
    // A new tab or window still gets the file itself.
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    open(link);
  });
})();
