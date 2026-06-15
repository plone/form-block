import React from 'react';
import BlockDataForm from '@plone/volto/components/manage/Form/BlockDataForm';
import { useIntl } from 'react-intl';
import type { JSONSchema } from '@plone/types';
import { schemaFormBlockSchema } from '@plone/volto-form-block/components/Blocks/SchemaForm/schema';

export interface SchemaFormBlockData {
  '@type'?: string;
  title?: string;
  description?: string;
  schema?: JSONSchema;
  captcha?: string;
  confirmation_recipients?: string;
  show_cancel?: boolean;
  submit_label?: string;
  cancel_label?: string;
  [key: string]: any;
}

interface SchemaFormBlockDataProps {
  data: SchemaFormBlockData;
  block: string;
  onChangeBlock: (block: string, data: SchemaFormBlockData) => void;
  navRoot?: any;
  contentType?: string;
  [key: string]: any;
}

/**
 * Wrap a `confirmation_recipients` value in the `${...}` template marker the
 * backend expects; pass other values through untouched.
 */
const wrapRecipients = (value?: string): string | undefined =>
  value ? '${' + value + '}' : value;

const SchemaFormBlockDataForm: React.FC<SchemaFormBlockDataProps> = (props) => {
  const { data, block, onChangeBlock, navRoot, contentType } = props;
  const intl = useIntl();
  // The schema builder reads the raw block-edit props plus `intl` (as the old
  // class passed `this.props`). Bridge the nominal cross-package mismatch
  // (react-intl's IntlShape vs @plone/types', index-signature props) via unknown.
  const schema = schemaFormBlockSchema({
    ...props,
    intl,
  } as unknown as Parameters<typeof schemaFormBlockSchema>[0]);

  return (
    <BlockDataForm
      schema={schema}
      title={schema.title}
      onChangeField={(id: string, value: any) => {
        onChangeBlock(block, {
          ...data,
          [id]:
            id === 'confirmation_recipients' ? wrapRecipients(value) : value,
        });
      }}
      onChangeBlock={(nextBlock: string, nextData: SchemaFormBlockData) => {
        onChangeBlock(nextBlock, {
          ...nextData,
          confirmation_recipients: wrapRecipients(
            nextData.confirmation_recipients,
          ),
        });
      }}
      formData={{
        ...data,
        confirmation_recipients: data.confirmation_recipients
          ? data.confirmation_recipients.replace(/[${}]/g, '')
          : data.confirmation_recipients,
      }}
      block={block}
      navRoot={navRoot}
      contentType={contentType}
    />
  );
};

export default SchemaFormBlockDataForm;
