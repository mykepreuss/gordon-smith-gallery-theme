/* The Permanent Collection's two finders (DESIGN.md §6.13, DS-62). Both improve pages that work
   without them (DS-19): the Artists page lists every artist, and the browse and artist pages reach
   every work.

   1. Artists A to Z ([data-gs-index]): a field that narrows the list as you type. Every word must
      appear in the artist's names (name, full name, other names), accents ignored.
   2. Collection search ([data-gs-finder]): works found by artist, title, year, category, medium or
      theme, shown as artwork tiles 48 at a time. Shopify's search doesn't look in entries, so the
      works come from sections/gs-collection-data, 250 to a request, the first time they're needed.
      On the site's search page ([data-gs-finder-site]) it shows the first few matches for the
      search already made, with a link to all of them on the Permanent Collection page. */
(() => {
  if (window.gsCollection) return;
  window.gsCollection = true;

  const fold = (s) => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const words = (s) => fold(s).split(/\s+/).filter(Boolean);
  const say = (el, key, count, terms) =>
    (el.dataset[key] || '').replace('[count]', count.toLocaleString('en-CA')).replace('[terms]', terms);

  /* ---------- 1. Artists A to Z ---------- */
  document.querySelectorAll('[data-gs-index]').forEach((index) => {
    const tools = index.querySelector('[data-gs-index-tools]');
    const input = tools && tools.querySelector('input');
    const status = index.querySelector('[role="status"]');
    const letters = index.querySelector('[data-gs-letters]');
    if (!input) return;
    const items = [...index.querySelectorAll('[data-gs-names]')].map((li) => ({ li, names: fold(li.dataset.gsNames) }));
    const groups = [...index.querySelectorAll('.gs-index__group')];
    // The letter bar gets its hairline only while it's stuck over the names (DS-65). It sticks at
    // -1px, so once stuck its top pixel is off screen and it's no longer wholly visible.
    if (letters && 'IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => {
        letters.toggleAttribute('data-stuck', entry.intersectionRatio < 1 && entry.boundingClientRect.top < 0);
      }, { threshold: [1] }).observe(letters);
    }
    tools.hidden = false;
    let timer;
    // The list narrows on every keystroke (it takes a few milliseconds); only the spoken count
    // waits for a pause in typing, so it isn't read out letter by letter.
    input.addEventListener('input', () => {
      const want = words(input.value);
      let shown = 0;
      items.forEach(({ li, names }) => {
        const match = want.every((w) => names.includes(w));
        li.hidden = !match;
        if (match) shown += 1;
      });
      groups.forEach((g) => { g.hidden = !g.querySelector('.gs-index__item:not([hidden])'); });
      if (letters) letters.hidden = want.length > 0;
      const terms = input.value.trim();
      clearTimeout(timer);
      timer = setTimeout(() => {
        status.textContent = !want.length ? '' : shown === 0 ? say(status, 'gsNone', 0, terms)
          : say(status, shown === 1 ? 'gsOne' : 'gsOther', shown, terms);
      }, 120);
    });
  });

  /* ---------- 2. Collection search ---------- */
  let works = null;
  async function loadWorks() {
    if (works) return works;
    const root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';
    // Shopify names the page parameter for a list of entries itself (page_<id>, not page), so the
    // first response says what it is.
    let param = 'page';
    const page = async (n) => {
      const url = n === 1 ? `${root}?section_id=gs-collection-data` : `${root}?section_id=gs-collection-data&${param}=${n}`;
      const res = await fetch(url, { credentials: 'same-origin' });
      if (!res.ok) throw new Error(res.status);
      const doc = new DOMParser().parseFromString(await res.text(), 'text/html');
      const data = doc.querySelector('[data-gs-collection-data]');
      if (data.dataset.param) param = data.dataset.param;
      return { pages: Number(data.dataset.pages) || 1, list: JSON.parse(data.textContent) };
    };
    // A failed load isn't kept: the next search (or focus) tries again.
    works = (async () => {
      const first = await page(1);
      const rest = await Promise.all(Array.from({ length: first.pages - 1 }, (_, i) => page(i + 2)));
      return [first, ...rest].flatMap((p) => p.list).map((w) => ({
        ...w, text: fold([w.a, w.t, w.y, w.c, w.m, w.k].join(' ')),
      }));
    })().catch((e) => { works = null; throw e; });
    return works;
  }

  function tile(w) {
    const li = document.createElement('li');
    const art = document.createElement('article');
    art.className = 'gs-artwork-tile';
    if (w.i) {
      const media = document.createElement('div');
      media.className = 'gs-media gs-media--artwork gs-shape-md';
      const img = document.createElement('img');
      img.src = w.i;
      img.alt = w.l || '';
      img.loading = 'lazy';
      img.decoding = 'async';
      if (w.r) { img.width = 600; img.height = Math.round(600 / Number(w.r)); }
      media.append(img);
      art.append(media);
    }
    if (w.a) {
      const artist = document.createElement('p');
      artist.className = 'gs-artwork-tile__artist';
      artist.textContent = w.a;
      art.append(artist);
    }
    const h = document.createElement('h3');
    h.className = 'gs-artwork-tile__title';
    const a = document.createElement('a');
    a.href = w.u;
    const cite = document.createElement('cite');
    cite.textContent = w.t;
    a.append(cite);
    if (w.y) a.append(`, ${w.y}`);
    h.append(a);
    art.append(h);
    if (w.m) {
      const m = document.createElement('p');
      m.className = 'gs-meta gs-artwork-tile__medium';
      m.textContent = w.m;
      art.append(m);
    }
    li.append(art);
    return li;
  }

  document.querySelectorAll('[data-gs-finder]').forEach((finder) => {
    const form = finder.querySelector('[data-gs-finder-form]');
    const input = form && form.querySelector('input');
    const status = finder.querySelector('[data-gs-finder-status]');
    const list = finder.querySelector('[data-gs-finder-results]');
    const more = finder.querySelector('[data-gs-finder-more]');
    const site = finder.hasAttribute('data-gs-finder-site');
    const limit = Number(finder.dataset.gsLimit) || 48;
    let matches = [];
    let shown = 0;
    let run = 0;

    // From the Show more button, focus moves to the first new work, so it isn't lost when the
    // button goes away after the last batch, and the next Tab doesn't skip the new works.
    const showMore = (fromClick) => {
      const first = shown;
      matches.slice(shown, shown + limit).forEach((w) => list.append(tile(w)));
      shown = Math.min(matches.length, shown + limit);
      if (more) more.hidden = site || shown >= matches.length;
      const link = fromClick === true && list.children[first] && list.children[first].querySelector('a');
      if (link) link.focus({ preventScroll: true });
    };

    async function search(q, push) {
      const want = words(q);
      const mine = ++run;
      list.replaceChildren();
      shown = 0;
      if (more) more.hidden = true;
      if (!want.length) { status.textContent = ''; matches = []; return; }
      status.textContent = status.dataset.gsLoading || '';
      let all;
      try { all = await loadWorks(); } catch (e) {
        if (mine === run) status.textContent = status.dataset.gsError || '';
        return;
      }
      if (mine !== run) return;
      matches = all.filter((w) => want.every((x) => w.text.includes(x)));
      const terms = q.trim();
      status.textContent = matches.length === 0 ? say(status, 'gsNone', 0, terms)
        : say(status, matches.length === 1 ? 'gsOne' : 'gsOther', matches.length, terms);
      if (site) finder.hidden = matches.length === 0;
      // The search page's own "Nothing found" gives way when the collection has matches.
      if (site) document.querySelector('[data-gs-finder-empty]')?.toggleAttribute('hidden', matches.length > 0);
      showMore();
      if (push) {
        const url = new URL(window.location.href);
        if (terms) url.searchParams.set('q', terms); else url.searchParams.delete('q');
        window.history.replaceState(null, '', url);
      }
    }

    if (site) {
      search(finder.dataset.gsQuery || '', false);
      return;
    }
    if (!form || !input) return;
    form.hidden = false;
    let timer;
    input.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(() => search(input.value, true), 200);
    });
    input.addEventListener('focus', () => { loadWorks().catch(() => {}); }, { once: true });
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      clearTimeout(timer);
      search(input.value, true);
    });
    if (more) more.querySelector('button').addEventListener('click', () => showMore(true));
    const q = new URL(window.location.href).searchParams.get('q');
    if (q) { input.value = q; search(q, false); }
  });
})();
