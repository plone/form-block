import { defineMessages, type MessageDescriptor } from 'react-intl';
import config from '@plone/volto/registry';
import map from 'lodash/map';
import keys from 'lodash/keys';
import filter from 'lodash/filter';
import type { BlockSchemaArgs, JSONSchema } from '@plone/types';
import type { SchemaFormConfig } from '@plone/volto-form-block/types/blocks';

const messages = defineMessages({
  form: {
    id: 'Form',
    defaultMessage: 'Form',
  },
  title: {
    id: 'Title',
    defaultMessage: 'Title',
  },
  description: {
    id: 'Description',
    defaultMessage: 'Description',
  },
  submit_label: {
    id: 'Submit button label',
    defaultMessage: 'Submit button label',
  },
  show_cancel: {
    id: 'Show cancel button',
    defaultMessage: 'Show cancel button',
  },
  cancel_label: {
    id: 'Cancel button label',
    defaultMessage: 'Cancel button label',
  },
  cancel: {
    id: 'Cancel',
    defaultMessage: 'Cancel',
  },
  submit: {
    id: 'Submit',
    defaultMessage: 'Submit',
  },
  captcha: {
    id: 'captcha',
    defaultMessage: 'Captcha provider',
  },
  send: {
    id: 'Send email to admin',
    defaultMessage: 'Send email to admin',
  },
  send_description: {
    id: 'send_description',
    defaultMessage:
      'When activated, an email will be sent to the admin recipients (see below) when a form is submitted',
  },
  recipients: {
    id: 'Admin email',
    defaultMessage: 'Admin email',
  },
  forward_user_to: {
    id: 'forward_user_to',
    defaultMessage: 'Forward user to',
  },
  forward_user_to_description: {
    id: 'forward_user_to_description',
    defaultMessage:
      'If a page is specified, the user will be directed there after submitting the form. The thank you message will not be displayed.',
  },
  success: {
    id: 'success',
    defaultMessage: 'Success message',
  },
  success_default: {
    id: 'success_default',
    defaultMessage: 'Thank you! You have submitted the following data:',
  },
  thankyou: {
    id: 'thankyou',
    defaultMessage: 'Thank you message',
  },
  thankyou_description: {
    id: 'thankyou_description',
    defaultMessage:
      "A text with simple formatting can be entered. Also it is possible to use variables; $'{field_id}' can be used to display the value of a field inside the form. The $'{formfields}' variable lists all form fields in a tabular view.",
  },
  recipients_description: {
    id: 'The email addresses the submitted form data will be sent to. Multiple email addresses can be entered separated by a semicolon.',
    defaultMessage:
      'The email addresses the submitted form data will be sent to. Multiple email addresses can be entered separated by a semicolon.',
  },
  bcc: {
    id: 'Blind copy',
    defaultMessage: 'Blind copy',
  },
  bcc_description: {
    id: 'The email addresses the submitted form data will be sent to as blind carbon copy. Multiple email addresses can be entered separated by a semicolon.',
    defaultMessage:
      'The email addresses the submitted form data will be sent to as blind carbon copy. Multiple email addresses can be entered separated by a semicolon.',
  },
  admin_info: {
    id: 'admin_info',
    defaultMessage: 'Admin info',
  },
  admin_info_description: {
    id: 'admin_info_description',
    defaultMessage:
      'This field can be used to store additional information which should only be displayed in the email sent to the administration email (not for the user email).',
  },
  http_headers: {
    id: 'http_headers',
    defaultMessage: 'HTTP Headers',
  },
  http_headers_description: {
    id: 'http_headers_description',
    defaultMessage:
      'HTTP headers to be included in the email sent to the administration email (not for the user email), one per line. Exemple: X-Forwarded-For, User-Agent, Referer. The values will be taken from the request headers.',
  },
  sender: {
    id: 'Sender',
    defaultMessage: 'Sender',
  },
  sender_description: {
    id: 'The email address of the sender',
    defaultMessage: 'The email address of the sender.',
  },
  sender_name: {
    id: 'Sender name',
    defaultMessage: 'Sender name',
  },
  sender_name_description: {
    id: 'The name of the sender',
    defaultMessage: 'The name of the sender.',
  },
  subject: {
    id: 'Subject',
    defaultMessage: 'Subject',
  },
  subject_description: {
    id: 'The subject used in the sent email.',
    defaultMessage: 'The subject used in the sent email.',
  },
  mail_header: {
    id: 'Email header',
    defaultMessage: 'Email header',
  },
  mail_header_description: {
    id: 'Text at the beginning of the email.',
    defaultMessage: 'Text at the beginning of the email.',
  },
  mail_footer: {
    id: 'Email footer',
    defaultMessage: 'Email footer',
  },
  mail_footer_description: {
    id: 'Text at the end of the email.',
    defaultMessage: 'Text at the end of the email.',
  },
  fieldset_store: {
    id: 'Store data',
    defaultMessage: 'Store data',
  },
  store: {
    id: 'Store data',
    defaultMessage: 'Store data',
  },
  store_description: {
    id: 'When activated, the data will be stored for later use when the form is submitted',
    defaultMessage:
      'When activated, the data will be stored for later use when the form is submitted',
  },
  data_wipe: {
    id: 'Data wipe',
    defaultMessage: 'Data wipe',
  },
  data_wipe_description: {
    id: 'Number of days after which, the data should be deleted. Enter -1 to store indefinitely.',
    defaultMessage:
      'Number of days after which, the data should be deleted. Enter -1 to store indefinitely.',
  },
  fieldset_mailing: {
    id: 'fieldset_mailing',
    defaultMessage: 'Mailing',
  },
  send_confirmation: {
    id: 'send_confirmation',
    defaultMessage: 'Send confirmation email',
  },
  confirmation_recipients: {
    id: 'confirmation_recipients',
    defaultMessage: 'Recipient',
  },
  confirmation_recipients_description: {
    id: 'confirmation_recipients_description',
    defaultMessage:
      'Send confirmation to the email entered in the following field',
  },
  fixed_attachment: {
    id: 'fixed_attachment',
    defaultMessage: 'Fixed attachment',
  },
  fieldset_confirmation: {
    id: 'fieldset_confirmation',
    defaultMessage: 'Confirmation-Page',
  },
  mail_template: {
    id: 'mail_template',
    defaultMessage: 'Mail template',
  },
});

const defaultEmptyData = {
  fieldsets: [
    {
      id: 'default',
      title: 'Default',
      fields: [],
    },
  ],
  properties: {},
  required: [],
};

/** The intl object of Volto's block schema arguments. */
export type SchemaFormIntl = NonNullable<BlockSchemaArgs['intl']>;

export interface SchemaFormBlockSchemaArgs {
  intl?: SchemaFormIntl;
}

export interface SchemaFormData {
  schema?: { properties?: Record<string, any> };
  [key: string]: any;
}

export interface SchemaFormConditionsArgs {
  data?: SchemaFormData;
  content?: { title?: string; [key: string]: any };
}

interface SchemaFieldset {
  id: string;
  title: string;
  fields: string[];
}

/**
 * Defaults of the schemaForm block configuration. They apply where the
 * registry has no configuration, such as on the server, which builds the
 * schema for the @blocks-schema endpoint. A registry value overrides them.
 */
export const schemaFormDefaults = {
  captchaProvidersVocabulary: 'plone.formblock.captcha.providers',
  mailTemplatesVocabulary: 'plone.formblock.mail.templates',
  defaultSender: 'noreply@plone.org',
  defaultSenderName: 'Plone',
};

/**
 * The settings schema of the schemaForm block, with every field.
 *
 * It takes only intl, so the @blocks-schema endpoint can build it outside the
 * editor. The fields that depend on the settings are shown, and their
 * requirements are set, by applySchemaFormConditions in the editor.
 *
 * @param {Object} args The arguments, with the intl object.
 * @returns {Object} The JSON schema of the block settings.
 */
export const schemaFormBlockSchema = ({
  intl,
}: SchemaFormBlockSchemaArgs = {}): JSONSchema => {
  // Without intl, as on a call that has no translations, the default texts are used.
  const formatMessage = (message: MessageDescriptor): string =>
    intl
      ? (intl.formatMessage(message as any) as string)
      : String(message.defaultMessage);
  const blockConfig = {
    ...schemaFormDefaults,
    ...(config.blocks?.blocksConfig?.schemaForm as
      | Partial<SchemaFormConfig>
      | undefined),
  };

  return {
    title: formatMessage(messages.form),
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: [
          'title',
          'description',
          'submit_label',
          'show_cancel',
          'cancel_label',
          'captcha',
        ],
      },
      {
        id: 'confirmation',
        title: formatMessage(messages.fieldset_confirmation),
        fields: ['forward_user_to', 'success', 'thankyou'],
      },
      {
        id: 'mailing',
        title: formatMessage(messages.fieldset_mailing),
        fields: [
          'send_confirmation',
          'confirmation_recipients',
          'fixed_attachment',
          'mail_template',
          'send',
          'recipients',
          'bcc',
          'admin_info',
          'httpHeaders',
          'sender',
          'sender_name',
          'subject',
          'mail_header',
          'mail_footer',
        ],
      },
      {
        id: 'savedata',
        title: formatMessage(messages.fieldset_store),
        fields: ['store', 'data_wipe'],
      },
    ],
    properties: {
      schema: {
        title: 'Schema',
        default: defaultEmptyData,
      },
      title: {
        title: formatMessage(messages.title),
      },
      description: {
        title: formatMessage(messages.description),
        widget: 'textarea',
      },
      submit_label: {
        title: formatMessage(messages.submit_label),
        default: formatMessage(messages.submit),
      },
      show_cancel: {
        type: 'boolean',
        title: formatMessage(messages.show_cancel),
        default: false,
      },
      cancel_label: {
        title: formatMessage(messages.cancel_label),
        default: formatMessage(messages.cancel),
      },
      forward_user_to: {
        title: formatMessage(messages.forward_user_to),
        description: formatMessage(messages.forward_user_to_description),
        widget: 'object_browser',
        mode: 'link',
        allowExternals: true,
      },
      success: {
        type: 'string',
        title: formatMessage(messages.success),
        default: formatMessage(messages.success_default),
      },
      thankyou: {
        type: 'string',
        title: formatMessage(messages.thankyou),
        description: formatMessage(messages.thankyou_description),
        widget: 'textarea',
        default: '${formfields}', // eslint-disable-line no-template-curly-in-string
      },
      captcha: {
        title: formatMessage(messages.captcha),
        type: 'string',
        factory: 'Choice',
        vocabulary: {
          '@id': blockConfig.captchaProvidersVocabulary,
        },
      },
      send: {
        type: 'boolean',
        title: formatMessage(messages.send),
        description: formatMessage(messages.send_description),
      },
      recipients: {
        title: formatMessage(messages.recipients),
        description: formatMessage(messages.recipients_description),
      },
      bcc: {
        title: formatMessage(messages.bcc),
        description: formatMessage(messages.bcc_description),
      },
      admin_info: {
        title: formatMessage(messages.admin_info),
        description: formatMessage(messages.admin_info_description),
        widget: 'textarea',
      },
      httpHeaders: {
        title: formatMessage(messages.http_headers),
        description: formatMessage(messages.http_headers_description),
        widget: 'textarea',
      },
      sender: {
        title: formatMessage(messages.sender),
        description: formatMessage(messages.sender_description),
        default: blockConfig.defaultSender,
      },
      sender_name: {
        title: formatMessage(messages.sender_name),
        description: formatMessage(messages.sender_name_description),
        default: blockConfig.defaultSenderName,
      },
      subject: {
        title: formatMessage(messages.subject),
        description: formatMessage(messages.subject_description),
      },
      mail_header: {
        title: formatMessage(messages.mail_header),
        widget: 'richtext',
        type: 'string',
        description: formatMessage(messages.mail_header_description),
      },
      mail_footer: {
        title: formatMessage(messages.mail_footer),
        widget: 'richtext',
        type: 'string',
        description: formatMessage(messages.mail_footer_description),
      },
      store: {
        type: 'boolean',
        title: formatMessage(messages.store),
        description: formatMessage(messages.store_description),
      },
      data_wipe: {
        type: 'integer',
        title: formatMessage(messages.data_wipe),
        description: formatMessage(messages.data_wipe_description),
        default: -1,
      },
      send_confirmation: {
        type: 'boolean',
        title: formatMessage(messages.send_confirmation),
      },
      confirmation_recipients: {
        title: formatMessage(messages.confirmation_recipients),
        description: intl.formatMessage(
          messages.confirmation_recipients_description,
        ),
      },
      fixed_attachment: {
        title: formatMessage(messages.fixed_attachment),
        type: 'object',
        widget: 'file',
      },
      mail_template: {
        title: formatMessage(messages.mail_template),
        type: 'string',
        factory: 'Choice',
        vocabulary: {
          '@id': blockConfig.mailTemplatesVocabulary,
        },
      },
    },
    required: [],
  };
};

/**
 * Applies the settings of a form to its schema, in the editor.
 *
 * It hides the fields of the settings that are off, sets the requirements of
 * the settings, lists the email fields of the form as confirmation recipients,
 * and defaults the subject to the title of the content.
 *
 * @param {Object} schema The schema from schemaFormBlockSchema.
 * @param {Object} args The settings of the block and the content it is in.
 * @returns {Object} The schema of the settings form.
 */
export const applySchemaFormConditions = (
  schema: JSONSchema,
  { data, content }: SchemaFormConditionsArgs,
): JSONSchema => {
  const hidden = new Set<string>();
  if (!data?.show_cancel) {
    hidden.add('cancel_label');
  }
  if (!data?.send_confirmation) {
    ['confirmation_recipients', 'fixed_attachment', 'mail_template'].forEach(
      (field) => hidden.add(field),
    );
  }
  if (!data?.send) {
    ['recipients', 'bcc', 'admin_info', 'httpHeaders'].forEach((field) =>
      hidden.add(field),
    );
  }
  if (!data?.send && !data?.send_confirmation) {
    ['sender', 'sender_name', 'subject', 'mail_header', 'mail_footer'].forEach(
      (field) => hidden.add(field),
    );
  }
  if (!data?.store) {
    hidden.add('data_wipe');
  }

  const required: string[] = [];
  if (data?.store !== true && data?.send !== true) {
    required.push('store', 'send');
  }
  if (data?.send_confirmation) {
    required.push('confirmation_recipients');
  }

  const formProperties = data?.schema?.properties || {};
  const emailFields = filter(
    keys(formProperties),
    (field) =>
      formProperties[field].factory === 'label_email' ||
      formProperties[field].factory === 'Email',
  );

  return {
    ...schema,
    fieldsets: (schema.fieldsets as SchemaFieldset[]).map((fieldset) => ({
      ...fieldset,
      fields: fieldset.fields.filter((field) => !hidden.has(field)),
    })),
    properties: {
      ...schema.properties,
      subject: {
        ...schema.properties.subject,
        default: content?.title,
      },
      confirmation_recipients: {
        ...schema.properties.confirmation_recipients,
        choices: map(emailFields, (field) => [
          field,
          formProperties[field].title,
        ]),
      },
    },
    required,
  };
};
