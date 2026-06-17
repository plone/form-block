import { describe, it, expect } from 'vitest';
import type { CellContext } from '@tanstack/react-table';
import type { IntlShape } from 'react-intl';
import type { StoredFormItem } from '@plone/volto-form-block/helpers/datatable';
import { buildColumns } from './columns';

const intl = {
  formatMessage: (descriptor: { defaultMessage?: string }) =>
    descriptor.defaultMessage,
} as unknown as IntlShape;

const items: StoredFormItem[] = [
  {
    block_id: { value: 'b1' },
    name: { value: 'Ada', label: 'Name', field_type: 'text' },
    agree: { value: true, label: 'Agree', field_type: 'checkbox' },
    date: { value: '2026-06-17', label: 'Date', field_type: 'date' },
  },
];

// react-table types accessorFn/cell as optional on the union; narrow for tests.
const accessorOf = (col: any) => col.accessorFn as (row: StoredFormItem) => any;
const cellOf = (col: any) =>
  col.cell as (props: CellContext<StoredFormItem, any>) => unknown;

describe('buildColumns', () => {
  it('produces one column per visible field, with date last', () => {
    expect(buildColumns(items, intl).map((c) => c.id)).toEqual([
      'name',
      'agree',
      'date',
    ]);
  });

  it('uses the field label as the column header', () => {
    const name = buildColumns(items, intl).find((c) => c.id === 'name');
    expect(name?.header).toBe('Name');
  });

  it('reads a row value via the column accessor', () => {
    const name = buildColumns(items, intl).find((c) => c.id === 'name');
    expect(accessorOf(name)(items[0])).toBe('Ada');
  });

  it('delegates cell rendering to the field-type renderer', () => {
    const agree = buildColumns(items, intl).find((c) => c.id === 'agree');
    const out = cellOf(agree)({ getValue: () => true } as CellContext<
      StoredFormItem,
      any
    >);
    expect(out).toBe('Yes');
  });
});
