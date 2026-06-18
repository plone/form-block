import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import DataTableActions from './DataTableActions';
import './DataTable.css';

const meta = {
  title: 'Components/DataTable/Actions',
  component: DataTableActions,
  decorators: [
    (Story) => (
      <div className="dt-wrapper" style={{ width: 720, padding: 16 }}>
        <Story />
      </div>
    ),
  ],
  parameters: { layout: 'padded' },
  tags: ['autodocs'],
  argTypes: {
    count: { control: { type: 'number', min: 0 } },
    onExport: { action: 'export' },
    onClear: { action: 'clear' },
  },
} satisfies Meta<typeof DataTableActions>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithSubmissions: Story = {
  args: { count: 12 },
};

export const SingleSubmission: Story = {
  args: { count: 1 },
};

export const Empty: Story = {
  args: { count: 0 },
};
