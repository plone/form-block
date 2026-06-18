import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';
import * as ReactTableLib from '@tanstack/react-table';
import type { StoredFormItem } from '@plone/volto-form-block/helpers/datatable';
import DataTable from './DataTable';

const BLOCK_ID = 'form-block-1';

const properties = { '@id': '/contact', id: 'contact' };

const sampleItems: StoredFormItem[] = [
  {
    block_id: { value: BLOCK_ID },
    name: { label: 'Name', field_type: 'text', value: 'Ada Lovelace' },
    email: { label: 'Email', field_type: 'email', value: 'ada@example.org' },
    message: {
      label: 'Message',
      field_type: 'textarea',
      value: 'Looking forward to the event.',
    },
    agree: { label: 'Agree to terms', field_type: 'checkbox', value: true },
    date: { label: 'Date', field_type: 'date', value: '2026-06-12' },
  },
  {
    block_id: { value: BLOCK_ID },
    name: { label: 'Name', field_type: 'text', value: 'Alan Turing' },
    email: { label: 'Email', field_type: 'email', value: 'alan@example.org' },
    message: {
      label: 'Message',
      field_type: 'textarea',
      value: 'Count me in.',
    },
    agree: { label: 'Agree to terms', field_type: 'checkbox', value: false },
    date: { label: 'Date', field_type: 'date', value: '2026-06-15' },
  },
  {
    block_id: { value: BLOCK_ID },
    name: { label: 'Name', field_type: 'text', value: 'Grace Hopper' },
    email: { label: 'Email', field_type: 'email', value: 'grace@example.org' },
    message: {
      label: 'Message',
      field_type: 'textarea',
      value: 'See you there.',
    },
    agree: { label: 'Agree to terms', field_type: 'checkbox', value: true },
    date: { label: 'Date', field_type: 'date', value: '2026-06-18' },
  },
];

/**
 * Seed the mock redux store with the slices the DataTable reads, plus the
 * pre-loaded `ReactTable` lazy library so `injectLazyLibs` resolves without
 * dispatching a load against the mock store.
 */
const storeWith = (items: StoredFormItem[]) => ({
  formData: {
    loaded: true,
    loading: false,
    error: null,
    result: { items },
  },
  clearFormData: { loaded: false, loading: false, error: null },
  lazyLibraries: { ReactTable: ReactTableLib },
});

const meta = {
  title: 'Components/DataTable/DataTable',
  component: DataTable,
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
} satisfies Meta<typeof DataTable>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithSubmissions: Story = {
  render: () => (
    <Wrapper location="/" customStore={storeWith(sampleItems)}>
      <div style={{ padding: 16 }}>
        <DataTable properties={properties} blockId={BLOCK_ID} />
      </div>
    </Wrapper>
  ),
};

export const NoSubmissions: Story = {
  render: () => (
    <Wrapper location="/" customStore={storeWith([])}>
      <div style={{ padding: 16 }}>
        <DataTable properties={properties} blockId={BLOCK_ID} />
      </div>
    </Wrapper>
  ),
};
