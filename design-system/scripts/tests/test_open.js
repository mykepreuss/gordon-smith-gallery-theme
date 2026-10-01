#!/usr/bin/env node
/*
 * Tests for js/gs-open.js: the "open today" line on set dates, with and without closures
 * (DS-54, DS-191). No browser: the page's line and the clock are stood in for.
 *
 *   node design-system/scripts/tests/test_open.js
 */
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, '..', '..', 'js', 'gs-open.js'), 'utf8');
const RealDate = Date;
const WEEK = 'Open Thursday to Saturday, 12 to 4 PM';

// The line as the page prints it, read at a moment (UTC) with the gallery in Vancouver.
function line(moment, closed) {
  const el = {
    textContent: WEEK,
    dataset: {
      tz: 'America/Vancouver', days: '4,5,6', opens: '12:00', closes: '16:00', closed,
      now: 'Open now until %time%', today: 'Open today, %times%',
      closedToday: 'Closed today. Open %day%, %times%', closedNow: 'Closed now. Open %day%, %times%',
      tomorrow: 'tomorrow', weekdays: 'Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday', to: 'to',
    },
  };
  const fixed = new RealDate(moment).getTime();
  global.document = { querySelectorAll: () => [el] };
  global.window = { Intl };
  global.Date = class extends RealDate {
    constructor(...args) { if (args.length) super(...args); else super(fixed); }
  };
  try {
    new Function(src)();
  } finally {
    global.Date = RealDate;
  }
  return el.textContent.replace(/ /g, ' ');
}

// The gallery's list for 2026 to 2027 (proposals/gallery-answers/, 1.2).
const CLOSED = [
  '2026-10-12/2026-10-12', '2026-11-11/2026-11-11', '2026-12-21/2027-01-01', '2027-02-15/2027-02-15',
  '2027-03-15/2027-03-29', '2027-05-24/2027-05-24', '2027-07-10/2027-08-22',
].join(',');

const cases = [
  // Without closures, as before.
  ['2026-10-01T20:00:00Z', '', 'Open now until 4 PM'],                                  // Thursday, 1 PM
  ['2026-10-01T18:00:00Z', '', 'Open today, 12 to 4 PM'],                               // Thursday, 11 AM
  ['2026-10-02T00:30:00Z', '', 'Closed now. Open tomorrow, 12 to 4 PM'],                // Thursday, 5:30 PM
  ['2026-10-04T20:00:00Z', '', 'Closed today. Open Thursday, 12 to 4 PM'],              // Sunday
  // A closure on a day the gallery is closed anyway changes nothing.
  ['2026-10-12T20:00:00Z', CLOSED, 'Closed today. Open Thursday, 12 to 4 PM'],
  // The last open day before the winter break, then the break.
  ['2026-12-19T20:00:00Z', CLOSED, 'Open now until 4 PM'],
  ['2026-12-20T01:00:00Z', CLOSED, 'Closed now. Open Saturday, January 2, 12 to 4 PM'],
  ['2026-12-24T20:00:00Z', CLOSED, 'Closed today. Open Saturday, January 2, 12 to 4 PM'], // a Thursday
  ['2027-01-01T20:00:00Z', CLOSED, 'Closed today. Open tomorrow, 12 to 4 PM'],
  ['2027-01-02T20:00:00Z', CLOSED, 'Open now until 4 PM'],
  // Spring break and the summer.
  ['2027-03-18T20:00:00Z', CLOSED, 'Closed today. Open Thursday, April 1, 12 to 4 PM'],
  ['2027-07-10T20:00:00Z', CLOSED, 'Closed today. Open Thursday, August 26, 12 to 4 PM'],
  ['2027-08-20T20:00:00Z', CLOSED, 'Closed today. Open Thursday, 12 to 4 PM'],
  ['2027-08-26T20:00:00Z', CLOSED, 'Open now until 4 PM'],
  // Closed for more than a year: the week's line stays, since there is no day to name.
  ['2026-10-04T20:00:00Z', '2026-01-01/2028-12-31', WEEK],
];

let failed = 0;
for (const [moment, closed, expected] of cases) {
  const got = line(moment, closed);
  try {
    assert.strictEqual(got, expected);
  } catch (e) {
    failed += 1;
    console.error(`FAIL ${moment}: expected "${expected}", got "${got}"`);
  }
}
console.log(`${cases.length - failed} of ${cases.length} passed`);
process.exit(failed ? 1 : 0);
