import type { SchemaFormConfig } from '@plone/volto-form-block/types/blocks';
import formSVG from '@plone/volto/icons/form.svg';
import { schemaFormBlockSchema } from '@plone/volto-form-block/components/Blocks/SchemaForm/schema';
import schemaFormBlockEdit from '@plone/volto-form-block/components/Blocks/SchemaForm/Edit';
import schemaFormBlockView from '@plone/volto-form-block/components/Blocks/SchemaForm/View';

const schemaFormBlock: SchemaFormConfig = {
  id: 'schemaForm',
  title: 'Form',
  icon: formSVG,
  group: 'text',
  view: schemaFormBlockView,
  edit: schemaFormBlockEdit,
  widgets: null,
  component: null,
  buttonComponent: null,
  blockSchema: schemaFormBlockSchema,
  captchaProvidersVocabulary: 'plone.formblock.captcha.providers',
  mailTemplatesVocabulary: 'plone.formblock.mail.templates',
  disableEnter: true,
  filterFactory: [
    'label_text_field',
    'label_choice_field',
    'label_boolean_field',
    'label_date_field',
    'label_datetime_field',
    'File Upload',
    'label_email',
    'radio_group',
    'checkbox_group',
    'hidden',
    'static_text',
    'number',
    'textarea',
    'time',
  ],
  additionalFactory: [
    { value: 'textarea', label: 'Textarea' },
    { value: 'radio_group', label: 'Radio Group' },
    { value: 'checkbox_group', label: 'Checkbox Group' },
    { value: 'hidden', label: 'Hidden' },
    { value: 'static_text', label: 'Static Text' },
    { value: 'number', label: 'Number' },
    { value: 'time', label: 'Time' },
  ],
  filterFactorySend: ['static_text'],
  defaultSender: 'noreply@plone.org',
  defaultSenderName: 'Plone',
  restricted: false,
  mostUsed: true,
  security: {
    addPermission: [],
    view: [],
  },
  sidebarTab: 1,
};

export default schemaFormBlock;
