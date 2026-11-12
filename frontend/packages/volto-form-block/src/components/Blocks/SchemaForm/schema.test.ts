import { describe, it, expect } from 'vitest';
import { createIntl } from 'react-intl';
import config from '@plone/volto/registry';
import {
  applySchemaFormConditions,
  schemaFormBlockSchema,
  type SchemaFormIntl,
} from '@plone/volto-form-block/components/Blocks/SchemaForm/schema';

const intl = createIntl({
  locale: 'en',
  messages: {},
}) as unknown as SchemaFormIntl;

const fieldsOf = (schema: any, fieldset: string): string[] =>
  schema.fieldsets.find((item: any) => item.id === fieldset).fields;

describe('schemaFormBlockSchema', () => {
  it('builds the complete settings schema with only intl, as the @blocks-schema endpoint calls it', () => {
    const schema: any = schemaFormBlockSchema({ intl });

    expect(schema.title).toBe('Form');
    expect(fieldsOf(schema, 'mailing')).toEqual(
      expect.arrayContaining(['send', 'recipients', 'sender', 'mail_footer']),
    );
    expect(fieldsOf(schema, 'savedata')).toEqual(['store', 'data_wipe']);
    expect(fieldsOf(schema, 'default')).toContain('cancel_label');
  });

  it('does not require any setting by itself, so the endpoint lists no conditional requirement', () => {
    const schema: any = schemaFormBlockSchema({ intl });

    expect(schema.required).toEqual([]);
  });

  it('uses the defaults of the block when the registry has no configuration', () => {
    const schema: any = schemaFormBlockSchema({ intl });

    expect(schema.properties.sender.default).toBe('noreply@plone.org');
    expect(schema.properties.sender_name.default).toBe('Plone');
    expect(schema.properties.mail_template.vocabulary['@id']).toBe(
      'plone.formblock.mail.templates',
    );
  });

  it('takes the email defaults of the registry over the defaults of the block', () => {
    const blocksConfig = config.blocks.blocksConfig as Record<string, any>;
    const previous = blocksConfig.schemaForm;
    blocksConfig.schemaForm = { defaultSender: 'site@example.org' };
    try {
      const schema: any = schemaFormBlockSchema({ intl });

      expect(schema.properties.sender.default).toBe('site@example.org');
      expect(schema.properties.sender_name.default).toBe('Plone');
    } finally {
      blocksConfig.schemaForm = previous;
    }
  });
});

describe('applySchemaFormConditions', () => {
  it('hides the fields of the settings that are off', () => {
    const schema: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      { data: { send: false, store: false, show_cancel: false } },
    );

    expect(fieldsOf(schema, 'mailing')).toEqual(['send_confirmation', 'send']);
    expect(fieldsOf(schema, 'savedata')).toEqual(['store']);
    expect(fieldsOf(schema, 'default')).not.toContain('cancel_label');
  });

  it('shows the mailing fields when send is on, and the sender fields for send_confirmation too', () => {
    const sending: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      { data: { send: true } },
    );
    expect(fieldsOf(sending, 'mailing')).toEqual(
      expect.arrayContaining(['recipients', 'bcc', 'sender', 'subject']),
    );
    expect(fieldsOf(sending, 'mailing')).not.toContain('mail_template');

    const confirming: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      { data: { send_confirmation: true } },
    );
    expect(fieldsOf(confirming, 'mailing')).toEqual(
      expect.arrayContaining([
        'confirmation_recipients',
        'mail_template',
        'sender',
      ]),
    );
    expect(fieldsOf(confirming, 'mailing')).not.toContain('recipients');
  });

  it('requires store or send, unless one of them is on', () => {
    const none: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      { data: {} },
    );
    expect(none.required).toEqual(['store', 'send']);

    const stored: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      { data: { store: true } },
    );
    expect(stored.required).toEqual([]);
  });

  it('requires the confirmation recipient when send_confirmation is on', () => {
    const schema: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      { data: { send: true, store: true, send_confirmation: true } },
    );

    expect(schema.required).toEqual(['confirmation_recipients']);
  });

  it('offers the email fields of the form as confirmation recipients', () => {
    const schema: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      {
        data: {
          schema: {
            properties: {
              name: { factory: 'label_text_field', title: 'Name' },
              email: { factory: 'label_email', title: 'E-mail' },
              contact: { factory: 'Email', title: 'Contact' },
            },
          },
        },
      },
    );

    expect(schema.properties.confirmation_recipients.choices).toEqual([
      ['email', 'E-mail'],
      ['contact', 'Contact'],
    ]);
  });

  it('uses the title of the content as the default subject', () => {
    const schema: any = applySchemaFormConditions(
      schemaFormBlockSchema({ intl }),
      { data: { send: true }, content: { title: 'Contact form' } },
    );

    expect(schema.properties.subject.default).toBe('Contact form');
  });
});
