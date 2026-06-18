import React from 'react';
import type { Meta, StoryFn } from '@storybook/react';
import HoneypotCaptchaWidget from './HoneypotCaptchaWidget';
import WidgetStory from '@plone/volto/components/manage/Widgets/story';

// On mount the widget writes a `captchaToken` value; a bot filling the
// (visually hidden) field would overwrite it. The Value panel shows the token.
export const Default = (WidgetStory as StoryFn).bind({
  props: {
    id: 'honeypot',
    captcha_props: { provider: 'honeypot' },
  },
  widget: HoneypotCaptchaWidget,
});

// In edit mode the widget renders nothing.
export const OnEdit = (WidgetStory as StoryFn).bind({
  props: {
    id: 'honeypot',
    onEdit: true,
    captcha_props: { provider: 'honeypot' },
  },
  widget: HoneypotCaptchaWidget,
});

const meta: Meta<typeof HoneypotCaptchaWidget> = {
  title: 'Widgets/HoneypotCaptcha',
  component: HoneypotCaptchaWidget,
  decorators: [
    (Story) => (
      <div style={{ width: '480px' }}>
        <h4>Honeypot captcha widget</h4>
        <Story />
      </div>
    ),
  ],
};

export default meta;
