import React, { useMemo } from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { useIntl } from 'react-intl';
import {
  getCoreRowModel,
  getPaginationRowModel,
  useReactTable,
} from '@tanstack/react-table';
import type { StoredFormItem } from '@plone/volto-form-block/helpers/datatable';
import { buildColumns } from './columns';
import DataTablePagination from './DataTablePagination';
import './DataTable.css';

const makeItems = (count: number): StoredFormItem[] =>
  Array.from({ length: count }, (_, i) => ({
    block_id: { value: 'form-1' },
    name: { label: 'Name', field_type: 'text', value: `Person ${i + 1}` },
    email: {
      label: 'Email',
      field_type: 'email',
      value: `person${i + 1}@example.org`,
    },
    date: {
      label: 'Date',
      field_type: 'date',
      value: `2026-06-${String((i % 28) + 1).padStart(2, '0')}`,
    },
  }));

/** Build a paginated react-table instance and render the pagination control. */
const PaginationDemo = ({
  count,
  pageSize = 5,
}: {
  count: number;
  pageSize?: number;
}) => {
  const intl = useIntl();
  const items = useMemo(() => makeItems(count), [count]);
  const columns = useMemo(() => buildColumns(items, intl), [items, intl]);
  const table = useReactTable({
    columns,
    data: items,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: { pagination: { pageIndex: 0, pageSize } },
  });
  return (
    <div className="dt-wrapper">
      <DataTablePagination table={table} />
    </div>
  );
};

const meta = {
  title: 'Components/DataTable/Pagination',
  component: DataTablePagination,
  parameters: { layout: 'padded' },
  tags: ['autodocs'],
} satisfies Meta<typeof DataTablePagination>;

export default meta;
type Story = StoryObj<typeof meta>;

export const TwoPages: Story = {
  render: () => <PaginationDemo count={8} pageSize={5} />,
};

export const ManyPages: Story = {
  render: () => <PaginationDemo count={42} pageSize={5} />,
};

// The control renders nothing for a single page (getPageCount() <= 1).
export const SinglePage: Story = {
  render: () => <PaginationDemo count={3} pageSize={5} />,
};
