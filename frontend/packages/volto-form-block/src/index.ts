import type { ConfigType } from '@plone/registry';
import installBlocks from '@plone/volto-form-block/config/blocks';
import installReducers from '@plone/volto-form-block/config/reducers';
import installSettings from '@plone/volto-form-block/config/settings';
import installWidgets from '@plone/volto-form-block/config/widgets';
import { defineMessages } from 'react-intl';

defineMessages({
  textarea: {
    id: 'textarea',
    defaultMessage: 'Textarea',
  },
  radio_group: {
    id: 'radio_group',
    defaultMessage: 'Radio Group',
  },
  checkbox_group: {
    id: 'checkbox_group',
    defaultMessage: 'Checkbox Group',
  },
  hidden: {
    id: 'hidden',
    defaultMessage: 'Hidden',
  },
  static_text: {
    id: 'static_text',
    defaultMessage: 'Static Text',
  },
  number: {
    id: 'number',
    defaultMessage: 'Number',
  },
  time: {
    id: 'time',
    defaultMessage: 'Time',
  },
});

function applyConfig(config: ConfigType) {
  installSettings(config);
  installReducers(config);
  installWidgets(config);
  installBlocks(config);

  return config;
}

export default applyConfig;
