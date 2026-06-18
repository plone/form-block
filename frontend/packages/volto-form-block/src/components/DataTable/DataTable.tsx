import { useMemo, useState, type FC } from 'react';
import { flattenToAppURL } from '@plone/volto/helpers/Url/Url';
import { injectLazyLibs } from '@plone/volto/helpers/Loadable/Loadable';
import { useIntl } from 'react-intl';
import { useDispatch } from 'react-redux';
import type { SortingState } from '@tanstack/react-table';
import type * as ReactTableLib from '@tanstack/react-table';
import { exportCsvFormData } from '@plone/volto-form-block/actions/exportCsv';
import { clearFormData } from '@plone/volto-form-block/actions/form';
import { buildColumns } from './columns';
import { useStoredFormData } from './useStoredFormData';
import DataTableActions from './DataTableActions';
import DataTableGrid from './DataTableGrid';
import DataTablePagination from './DataTablePagination';

import './DataTable.css';

/** The subset of the injected `@tanstack/react-table` lib this component uses. */
interface ReactTableModule {
  useReactTable: typeof ReactTableLib.useReactTable;
  flexRender: typeof ReactTableLib.flexRender;
  getCoreRowModel: typeof ReactTableLib.getCoreRowModel;
  getPaginationRowModel: typeof ReactTableLib.getPaginationRowModel;
  getSortedRowModel: typeof ReactTableLib.getSortedRowModel;
}

interface DataTableProps {
  ReactTable: ReactTableModule;
  properties: {
    '@id': string;
    id?: string;
    [key: string]: any;
  };
  blockId: string;
}

const DataTable: FC<DataTableProps> = ({ ReactTable, properties, blockId }) => {
  const {
    useReactTable,
    flexRender,
    getCoreRowModel,
    getPaginationRowModel,
    getSortedRowModel,
  } = ReactTable;
  const dispatch = useDispatch();
  const intl = useIntl();
  const path = flattenToAppURL(properties['@id']);

  const data = useStoredFormData(path, blockId);
  const [sorting, setSorting] = useState<SortingState>([]);
  const columns = useMemo(() => buildColumns(data, intl), [data, intl]);

  const table = useReactTable({
    columns,
    data,
    state: {
      sorting,
    },
    columnResizeMode: 'onEnd',
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="dt-wrapper">
      <DataTableActions
        count={data.length}
        onExport={() =>
          dispatch(
            exportCsvFormData(
              path,
              `export-${properties.id ?? 'form'}.csv`,
              blockId,
            ),
          )
        }
        onClear={() => dispatch(clearFormData(path, blockId))}
      />
      <DataTableGrid table={table} flexRender={flexRender} />
      <DataTablePagination table={table} />
    </div>
  );
};

export default injectLazyLibs(['ReactTable'])(DataTable);
