import type { CellContext, ColumnDef } from '@tanstack/react-table';
import type { IntlShape } from 'react-intl';
import {
  buildColumnOrder,
  getFieldMeta,
  type StoredFormItem,
} from '@plone/volto-form-block/helpers/datatable';
import { renderStoredFieldCell } from './Cells';

/**
 * Build the react-table column definitions for the stored submissions.
 *
 * Column identity and order come from :func:`buildColumnOrder`; each column's
 * header and cell rendering are derived from the field metadata.
 *
 * :param items: The stored submissions.
 * :param intl: The active react-intl shape, passed through to cell rendering.
 * :returns: Column definitions in display order.
 */
export function buildColumns(
  items: StoredFormItem[],
  intl: IntlShape,
): ColumnDef<StoredFormItem, any>[] {
  return buildColumnOrder(items).map((id) => {
    const meta = getFieldMeta(items, id);
    return {
      id,
      header: meta?.label,
      accessorFn: (row: StoredFormItem) => row[id]?.value,
      cell: (props: CellContext<StoredFormItem, any>) =>
        renderStoredFieldCell(meta?.field_type, props.getValue(), intl),
    };
  });
}
