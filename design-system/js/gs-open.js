/*
 * Gordon Smith Gallery: whether the gallery is open today (DESIGN.md §6.13, DS-54).
 * Theme copy: theme/assets/gs-open.js, loaded with `defer`.
 *
 * The page already says the week's hours ("Open Thursday to Saturday, 12 to 4 PM"), from
 * snippets/gs-open-today.liquid. This file turns that line into today's, in the gallery's own
 * time zone whatever the visitor's clock says:
 *
 *   open day, before opening   Open today, 12 to 4 PM
 *   open day, during hours     Open now until 4 PM
 *   open day, after closing    Closed now. Open Friday, 12 to 4 PM   ("tomorrow" when it is)
 *   closed day                 Closed today. Open Thursday, 12 to 4 PM
 *
 * Wording comes from the theme's locale file through data attributes. It runs once, on load.
 */
(() => {
  const lines = document.querySelectorAll('[data-gs-open]:not([data-gs-open-done])');
  if (!lines.length || !window.Intl) return;

  const WEEK = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  const minutes = (hhmm) => {
    const [h, m] = hhmm.split(':').map(Number);
    return h * 60 + m;
  };
  const clock = (total) => {
    const h = Math.floor(total / 60);
    const m = total % 60;
    const h12 = h % 12 || 12;
    return { text: m ? `${h12}:${String(m).padStart(2, '0')}` : `${h12}`, period: h < 12 ? 'AM' : 'PM' };
  };
  // "12 to 4 PM", "10 AM to 4 PM": the period shows once when both times share it. A no-break
  // space (\u00a0) keeps each time with its AM or PM; "to" can still break.
  const range = (opens, closes, to) => {
    const a = clock(opens);
    const b = clock(closes);
    return a.period === b.period
      ? `${a.text} ${to} ${b.text}\u00a0${b.period}`
      : `${a.text}\u00a0${a.period} ${to} ${b.text}\u00a0${b.period}`;
  };

  lines.forEach((el) => {
    const d = el.dataset;
    const days = (d.days || '').split(',').filter(Boolean).map(Number);
    if (!days.length) return;
    let now;
    try {
      now = Object.fromEntries(
        new Intl.DateTimeFormat('en-CA', {
          timeZone: d.tz, weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23',
        }).formatToParts(new Date()).map((p) => [p.type, p.value]),
      );
    } catch (e) {
      return; // An unknown time zone: keep the week's line.
    }
    const today = WEEK[now.weekday];
    const at = Number(now.hour) * 60 + Number(now.minute);
    const opens = minutes(d.opens);
    const closes = minutes(d.closes);
    const times = range(opens, closes, d.to);
    const names = d.weekdays.split(',');
    const next = () => {
      for (let i = 1; i <= 7; i += 1) {
        const day = (today + i) % 7;
        if (days.includes(day)) return i === 1 ? d.tomorrow : names[day];
      }
      return '';
    };

    let text;
    if (days.includes(today) && at < opens) {
      text = d.today.replace('%times%', times);
    } else if (days.includes(today) && at < closes) {
      const until = clock(closes);
      text = d.now.replace('%time%', `${until.text}\u00a0${until.period}`);
    } else {
      const template = days.includes(today) ? d.closedNow : d.closedToday;
      text = template.replace('%day%', next()).replace('%times%', times);
    }
    el.textContent = text;
    el.dataset.gsOpenDone = '';
  });
})();
