import { describe, it, expect } from 'vitest';
import {
  toLocalDateTimeString,
  serializeDateValue,
  parseDateValue,
  formatShortDate,
  formatLongDateTime,
} from './date';

describe('toLocalDateTimeString', () => {
  it('formats local components as YYYY-MM-DDTHH:mm:ss with zero-padding', () => {
    // Constructed from local parts, read back via local getters -> timezone agnostic.
    const d = new Date(2026, 0, 3, 4, 5, 6);
    expect(toLocalDateTimeString(d)).toBe('2026-01-03T04:05:06');
  });
});

describe('serializeDateValue', () => {
  it('serializes a date-only value as YYYY-MM-DD', () => {
    expect(serializeDateValue({ year: 2026, month: 6, day: 5 }, true)).toBe(
      '2026-06-05',
    );
  });

  it('zero-pads single-digit month and day', () => {
    expect(serializeDateValue({ year: 2026, month: 1, day: 9 }, true)).toBe(
      '2026-01-09',
    );
  });

  it('ignores time fields for date-only values', () => {
    expect(
      serializeDateValue(
        { year: 2026, month: 6, day: 5, hour: 23, minute: 59, second: 59 },
        true,
      ),
    ).toBe('2026-06-05');
  });

  it('serializes a datetime value as an ISO 8601 UTC string', () => {
    const iso = serializeDateValue(
      { year: 2026, month: 6, day: 5, hour: 14, minute: 30, second: 15 },
      false,
    );
    expect(iso).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
  });

  it('zeroes milliseconds in the datetime output', () => {
    const iso = serializeDateValue(
      { year: 2026, month: 6, day: 5, hour: 14, minute: 30, second: 15 },
      false,
    );
    expect(iso.endsWith('.000Z')).toBe(true);
  });

  it('defaults missing time fields to zero for datetime values', () => {
    const iso = serializeDateValue({ year: 2026, month: 6, day: 5 }, false);
    // Same instant as explicitly passing 0/0/0.
    expect(iso).toBe(new Date(2026, 5, 5, 0, 0, 0).toISOString());
  });
});

describe('parseDateValue', () => {
  it('parses a date-only value into a CalendarDate', () => {
    const parsed = parseDateValue('2026-06-05', true);
    expect(parsed.year).toBe(2026);
    expect(parsed.month).toBe(6);
    expect(parsed.day).toBe(5);
  });
});

describe('serialize/parse round-trip', () => {
  it('preserves the wall-clock calendar parts for datetime values', () => {
    const input = {
      year: 2026,
      month: 6,
      day: 5,
      hour: 14,
      minute: 30,
      second: 15,
    };
    const parsed = parseDateValue(serializeDateValue(input, false), false);
    expect(parsed.year).toBe(input.year);
    expect(parsed.month).toBe(input.month);
    expect(parsed.day).toBe(input.day);
    // CalendarDateTime exposes the time parts; CalendarDate would not.
    expect((parsed as { hour: number }).hour).toBe(input.hour);
    expect((parsed as { minute: number }).minute).toBe(input.minute);
    expect((parsed as { second: number }).second).toBe(input.second);
  });

  it('preserves the date for date-only values', () => {
    const input = { year: 2026, month: 1, day: 9 };
    const parsed = parseDateValue(serializeDateValue(input, true), true);
    expect(parsed.year).toBe(input.year);
    expect(parsed.month).toBe(input.month);
    expect(parsed.day).toBe(input.day);
  });
});

describe('formatShortDate', () => {
  it('formats a date-only value as a localized numeric date', () => {
    expect(formatShortDate('2026-06-15', 'en-US')).toBe('6/15/2026');
  });

  it('renders the stored calendar day regardless of timezone', () => {
    // A date-only value is rendered in UTC, so it must never slip to the
    // previous day in timezones behind UTC.
    expect(formatShortDate('2026-01-01', 'en-US')).toBe('1/1/2026');
  });

  it('returns an empty string for an invalid value', () => {
    expect(formatShortDate('not-a-date', 'en-US')).toBe('');
  });
});

describe('formatLongDateTime', () => {
  it('formats a datetime as a localized long date and time', () => {
    // A locally-constructed Date formatted in the local timezone is
    // timezone-agnostic, so the assertion is stable across runners.
    const out = formatLongDateTime(new Date(2026, 5, 15, 14, 30), 'en-US');
    expect(out).toContain('June');
    expect(out).toContain('15');
    expect(out).toContain('2026');
    expect(out).toContain('2:30');
    expect(out).toContain('PM');
  });

  it('returns an empty string for an invalid value', () => {
    expect(formatLongDateTime('nope', 'en-US')).toBe('');
  });
});
