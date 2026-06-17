import type { FC } from 'react';
import { Table } from 'semantic-ui-react';
import type { Table as ReactTableInstance } from '@tanstack/react-table';
import type * as ReactTableLib from '@tanstack/react-table';
import type { StoredFormItem } from '@plone/volto-form-block/helpers/datatable';

interface DataTableGridProps {
  /** The react-table instance driving the grid. */
  table: ReactTableInstance<StoredFormItem>;
  /** The injected `flexRender` helper from `@tanstack/react-table`. */
  flexRender: typeof ReactTableLib.flexRender;
}

/**
 * The sortable table grid rendering the stored submissions.
 */
const DataTableGrid: FC<DataTableGridProps> = ({ table, flexRender }) => {
  return (
    <div className="dt-wrapper-table">
      <Table celled sortable striped>
        <Table.Header>
          {table.getHeaderGroups().map((headerGroup) => (
            <Table.Row key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                const sortDir = header.column.getIsSorted();
                return (
                  <Table.HeaderCell
                    key={header.id}
                    sorted={
                      sortDir
                        ? sortDir === 'asc'
                          ? 'ascending'
                          : 'descending'
                        : undefined
                    }
                    onClick={header.column.getToggleSortingHandler()}
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                  </Table.HeaderCell>
                );
              })}
            </Table.Row>
          ))}
        </Table.Header>
        <Table.Body>
          {table.getRowModel().rows.map((row) => (
            <Table.Row key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <Table.Cell key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </Table.Cell>
              ))}
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>
  );
};

export default DataTableGrid;
