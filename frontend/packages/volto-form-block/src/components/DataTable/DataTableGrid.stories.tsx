import React, { useMemo, useState } from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { useIntl } from 'react-intl';
import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import type { StoredFormItem } from '@plone/volto-form-block/helpers/datatable';
import { buildColumns } from './columns';
import DataTableGrid from './DataTableGrid';
import './DataTable.css';

const sampleItems: StoredFormItem[] = [
  {
    block_id: { value: 'form-1' },
    name: { label: 'Name', field_type: 'text', value: 'Ada Lovelace' },
    email: { label: 'Email', field_type: 'email', value: 'ada@example.org' },
    message: {
      label: 'Message',
      field_type: 'textarea',
      value: 'Hello there!\nA second line.',
    },
    agree: { label: 'Agree to terms', field_type: 'checkbox', value: true },
    date: { label: 'Date', field_type: 'date', value: '2026-06-12' },
  },
  {
    block_id: { value: 'form-1' },
    name: { label: 'Name', field_type: 'text', value: 'Alan Turing' },
    email: { label: 'Email', field_type: 'email', value: 'alan@example.org' },
    message: { label: 'Message', field_type: 'textarea', value: 'Computable.' },
    agree: { label: 'Agree to terms', field_type: 'checkbox', value: false },
    date: { label: 'Date', field_type: 'date', value: '2026-06-15' },
  },
  {
    block_id: { value: 'form-1' },
    name: { label: 'Name', field_type: 'text', value: 'Grace Hopper' },
    email: { label: 'Email', field_type: 'email', value: 'grace@example.org' },
    message: {
      label: 'Message',
      field_type: 'textarea',
      value: 'Nanoseconds.',
    },
    agree: { label: 'Agree to terms', field_type: 'checkbox', value: true },
    date: { label: 'Date', field_type: 'date', value: '2026-06-18' },
  },
];

/** Build a real react-table instance and render the grid with it. */
const GridDemo = ({ items }: { items: StoredFormItem[] }) => {
  const intl = useIntl();
  const [sorting, setSorting] = useState<SortingState>([]);
  const columns = useMemo(() => buildColumns(items, intl), [items, intl]);
  const table = useReactTable({
    columns,
    data: items,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });
  return (
    <div className="dt-wrapper">
      <DataTableGrid table={table} flexRender={flexRender} />
    </div>
  );
};

const meta = {
  title: 'Components/DataTable/Grid',
  component: DataTableGrid,
  parameters: { layout: 'padded' },
  tags: ['autodocs'],
} satisfies Meta<typeof DataTableGrid>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithData: Story = {
  render: () => <GridDemo items={sampleItems} />,
};

export const SingleRow: Story = {
  render: () => <GridDemo items={[sampleItems[0]]} />,
};

export const Empty: Story = {
  render: () => <GridDemo items={[]} />,
};
