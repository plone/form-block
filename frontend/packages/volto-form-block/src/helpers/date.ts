/**
 * Date helpers.
 * @module helpers/date
 */
import {
  parseDate,
  parseDateTime,
  type CalendarDate,
  type CalendarDateTime,
} from '@internationalized/date';

/**
 * Calendar parts emitted by the date widget. Time fields are absent for
 * date-only fields.
 */
export type DateValue = {
  year: number;
  month: number;
  day: number;
  hour?: number;
  minute?: number;
  second?: number;
};

const pad = (n: number) => String(n).padStart(2, '0');

/**
 * Format a Date's *local* components as `YYYY-MM-DDTHH:mm:ss` (no timezone),
 * the timezone-free shape `@internationalized/date`'s `parseDateTime` expects.
 */
export const toLocalDateTimeString = (d: Date): string =>
  `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T` +
  `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;

/**
 * Serialize the calendar parts emitted by the date widget into the value
 * stored on the form: a `YYYY-MM-DD` string for date-only fields, or an
 * ISO 8601 UTC string for datetime fields.
 */
export function serializeDateValue(date: DateValue, dateOnly: boolean): string {
  if (dateOnly) {
    return `${date.year}-${pad(date.month)}-${pad(date.day)}`;
  }
  const dt = new Date(
    date.year,
    date.month - 1,
    date.day,
    date.hour ?? 0,
    date.minute ?? 0,
    date.second ?? 0,
  );
  return dt.toISOString();
}

/**
 * Parse a stored form value back into the `CalendarDate` / `CalendarDateTime`
 * the date widget expects. Datetime values are rendered as local wall-clock.
 */
export function parseDateValue(
  value: string,
  dateOnly: boolean,
): CalendarDate | CalendarDateTime {
  return dateOnly
    ? parseDate(value)
    : parseDateTime(toLocalDateTimeString(new Date(value)));
}

/**
 * Format a stored date-only value (`YYYY-MM-DD`) as a localized short date.
 * The value is a timezone-free calendar date, so it is rendered in UTC to keep
 * the displayed day stable across timezones (replacement for moment's `l`).
 */
export function formatShortDate(
  value: string | number | Date,
  locale: string,
): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return '';
  }
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    timeZone: 'UTC',
  }).format(date);
}

/**
 * Format a stored datetime value (ISO 8601) as a localized long date and time,
 * rendered in the viewer's local timezone (replacement for moment's `LLL`).
 */
export function formatLongDateTime(
  value: string | number | Date,
  locale: string,
): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return '';
  }
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date);
}
