import { describe, it, expect } from 'vitest';
import { isValidElement, type ReactElement } from 'react';
import type { IntlShape } from 'react-intl';
import { renderStoredFieldCell } from './Cells';

// Minimal intl stub: echo the message's default text.
const intl = {
  formatMessage: (descriptor: { defaultMessage?: string }) =>
    descriptor.defaultMessage,
} as unknown as IntlShape;

describe('renderStoredFieldCell', () => {
  it('renders an attachment as a download link', () => {
    const el = renderStoredFieldCell(
      'attachment',
      { url: '/f.pdf', filename: 'f.pdf' },
      intl,
    );
    expect(isValidElement(el)).toBe(true);
    const element = el as ReactElement<any>;
    expect(element.type).toBe('a');
    expect(element.props.href).toBe('/f.pdf');
    expect(element.props.download).toBe(true);
    expect(element.props.children).toBe('f.pdf');
  });

  it('renders an empty string for a missing attachment', () => {
    expect(renderStoredFieldCell('attachment', null, intl)).toBe('');
  });

  it('wraps textarea content in a pre element', () => {
    const el = renderStoredFieldCell(
      'textarea',
      'hello',
      intl,
    ) as ReactElement<any>;
    expect(el.type).toBe('pre');
    expect(el.props.children).toBe('hello');
  });

  it('renders checkbox values as localized yes/no', () => {
    expect(renderStoredFieldCell('checkbox', true, intl)).toBe('Yes');
    expect(renderStoredFieldCell('checkbox', false, intl)).toBe('No');
  });

  it('renders other field types as their raw value', () => {
    expect(renderStoredFieldCell('text', 'Ada', intl)).toBe('Ada');
    expect(renderStoredFieldCell('text', '', intl)).toBe('');
  });
});
