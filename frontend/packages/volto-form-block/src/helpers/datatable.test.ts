import { describe, it, expect } from 'vitest';
import {
  buildColumnOrder,
  getFieldMeta,
  selectBlockItems,
  type StoredFormItem,
} from './datatable';

const item = (overrides: StoredFormItem = {}): StoredFormItem => ({
  block_id: { value: 'block-1', label: 'Block', field_type: 'hidden' },
  name: { value: 'Ada', label: 'Name', field_type: 'text' },
  date: { value: '2026-06-17', label: 'Date', field_type: 'date' },
  ...overrides,
});

describe('selectBlockItems', () => {
  it('returns an empty array when there is no result', () => {
    expect(selectBlockItems(undefined, 'block-1')).toEqual([]);
    expect(selectBlockItems({}, 'block-1')).toEqual([]);
    expect(selectBlockItems({ result: { items: [] } }, 'block-1')).toEqual([]);
  });

  it('keeps only the items matching the block id', () => {
    const a = item();
    const b = item({ block_id: { value: 'block-2' } });
    expect(selectBlockItems({ result: { items: [a, b] } }, 'block-1')).toEqual([
      a,
    ]);
  });
});

describe('buildColumnOrder', () => {
  it('returns an empty array for no items', () => {
    expect(buildColumnOrder([])).toEqual([]);
  });

  it('excludes internal ids and forces date to the end', () => {
    expect(buildColumnOrder([item()])).toEqual(['name', 'date']);
  });

  it('de-duplicates ids across items, keeping first-seen order', () => {
    const a: StoredFormItem = {
      name: { value: 'Ada' },
      email: { value: 'a@x' },
    };
    const b: StoredFormItem = {
      email: { value: 'b@x' },
      phone: { value: '1' },
    };
    expect(buildColumnOrder([a, b])).toEqual(['name', 'email', 'phone']);
  });

  it('omits the date column when no item has one', () => {
    expect(buildColumnOrder([{ name: { value: 'Ada' } }])).toEqual(['name']);
  });
});

describe('getFieldMeta', () => {
  it('returns the field value from the first item that has the id', () => {
    expect(getFieldMeta([item()], 'name')).toEqual({
      value: 'Ada',
      label: 'Name',
      field_type: 'text',
    });
  });

  it('returns undefined for an unknown id', () => {
    expect(getFieldMeta([item()], 'missing')).toBeUndefined();
  });
});
