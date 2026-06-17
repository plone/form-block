/**
 * Pure helpers for the stored form-data table.
 * @module helpers/datatable
 */

/** A single stored field within a saved form submission. */
export interface StoredFieldValue {
  label?: string;
  value?: any;
  field_type?: string;
}

/** One stored submission: a map of field id to its stored value. */
export type StoredFormItem = Record<string, StoredFieldValue>;

/** Shape of the `formData` redux slice consumed by the DataTable. */
export interface FormDataState {
  result?: { items?: StoredFormItem[] };
}

/** Field ids that are never rendered as their own data column. */
export const EXCLUDE_COLUMN_IDS = ['__expired', 'block_id', 'id', 'field_type'];

/**
 * Select the stored submissions belonging to a given form block.
 *
 * :param formData: The ``formData`` redux slice.
 * :param blockId: The id of the form block whose submissions to keep.
 * :returns: The submissions whose ``block_id`` matches ``blockId``.
 */
export function selectBlockItems(
  formData: FormDataState | undefined,
  blockId: string,
): StoredFormItem[] {
  const items = formData?.result?.items;
  if (!items?.length) {
    return [];
  }
  return items.filter((item) => item.block_id?.value === blockId);
}

/**
 * Build the ordered, de-duplicated list of column ids to render.
 *
 * Excludes the internal ids in :data:`EXCLUDE_COLUMN_IDS`, keeps the first
 * occurrence of each id across all submissions, and forces a ``date`` column
 * to the end.
 *
 * :param items: The stored submissions.
 * :returns: The column ids in display order.
 */
export function buildColumnOrder(items: StoredFormItem[]): string[] {
  if (!items?.length) {
    return [];
  }
  const unique: string[] = [];
  for (const item of items) {
    for (const id of Object.keys(item)) {
      if (id && !EXCLUDE_COLUMN_IDS.includes(id) && !unique.includes(id)) {
        unique.push(id);
      }
    }
  }
  const ordered = unique.filter((id) => id !== 'date');
  if (unique.includes('date')) {
    ordered.push('date'); // Always render the date column last.
  }
  return ordered;
}

/**
 * Find the stored value (label, field type, value) for a column id.
 *
 * Reads from the first submission that contains the id, matching how column
 * metadata is derived in :func:`buildColumnOrder`.
 *
 * :param items: The stored submissions.
 * :param id: The column id to look up.
 * :returns: The matching field value, or ``undefined`` if no item has it.
 */
export function getFieldMeta(
  items: StoredFormItem[],
  id: string,
): StoredFieldValue | undefined {
  for (const item of items) {
    if (item[id] !== undefined) {
      return item[id];
    }
  }
  return undefined;
}
