import React from 'react';
import type { Meta, StoryFn } from '@storybook/react';
import NoRobotsCaptchaWidget from './NorobotsCaptchaWidget';
import WidgetStory from '@plone/volto/components/manage/Widgets/story';

// A question/answer captcha: the question is the field label, the answer is typed.
export const Default = (WidgetStory as StoryFn).bind({
  props: {
    id: 'norobots',
    captcha_props: {
      id: 'norobots',
      title: 'To prove you are human, what is 2 + 2?',
    },
  },
  widget: NoRobotsCaptchaWidget,
});

export const WithAnswer = (WidgetStory as StoryFn).bind({
  initialValue: '4',
  props: {
    id: 'norobots',
    captcha_props: {
      id: 'norobots',
      title: 'To prove you are human, what is 2 + 2?',
    },
  },
  widget: NoRobotsCaptchaWidget,
});

// In edit mode the widget renders nothing.
export const OnEdit = (WidgetStory as StoryFn).bind({
  props: {
    id: 'norobots',
    onEdit: true,
    captcha_props: {
      id: 'norobots',
      title: 'To prove you are human, what is 2 + 2?',
    },
  },
  widget: NoRobotsCaptchaWidget,
});

const meta: Meta<typeof NoRobotsCaptchaWidget> = {
  title: 'Widgets/NorobotsCaptcha',
  component: NoRobotsCaptchaWidget,
  decorators: [
    (Story) => (
      <div style={{ width: '480px' }}>
        <h4>No-robots question/answer captcha widget</h4>
        <Story />
      </div>
    ),
  ],
};

export default meta;
