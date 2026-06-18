/* eslint-disable no-template-curly-in-string */
import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import ThankYou from './ThankYou';

const meta = {
  title: 'Components/ThankYou',
  component: ThankYou,
  decorators: [
    (Story) => (
      <div className="ui segment" style={{ width: 640, padding: 16 }}>
        <Story />
      </div>
    ),
  ],
  parameters: { layout: 'padded' },
  tags: ['autodocs'],
  argTypes: {
    data: { control: 'object' },
    formfields: { control: 'text' },
    submittedData: { control: 'object' },
  },
} satisfies Meta<typeof ThankYou>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    data: {
      success: 'Your message has been sent.',
      thankyou:
        '<p>Thanks for getting in touch! Here is a copy of your submission:</p>${formfields}',
    },
    formfields:
      '<ul><li><strong>Name:</strong> Ada Lovelace</li><li><strong>Email:</strong> ada@example.org</li></ul>',
    submittedData: {
      name: 'Ada Lovelace',
      email: 'ada@example.org',
    },
  },
};

export const WithFieldInterpolation: Story = {
  args: {
    data: {
      success: 'Registration complete.',
      thankyou:
        '<p>Welcome, ${name}! A confirmation was sent to <em>${email}</em>.</p>',
    },
    formfields: '',
    submittedData: {
      name: 'Grace Hopper',
      email: 'grace@example.org',
    },
  },
};

export const MessageOnly: Story = {
  args: {
    data: {
      success: 'Thank you! Your response was recorded.',
      thankyou: '',
    },
    formfields: '',
    submittedData: {},
  },
};
