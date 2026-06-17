import React from 'react';
import isEmpty from 'lodash/isEmpty';
import { defineMessages, useIntl } from 'react-intl';
import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';
import { Form } from '@plone/volto/components/manage/Form';
import { withBlockExtensions } from '@plone/volto/helpers/Extensions';
import config from '@plone/volto/registry';
import { stripRequiredProperty } from '@plone/volto-form-block/helpers/schema';
import SchemaFormBlockDataForm from '@plone/volto-form-block/components/Blocks/SchemaForm/Data';
import type { SchemaFormBlockData } from '@plone/volto-form-block/components/Blocks/SchemaForm/Data';
import type { JSONSchema } from '@plone/types';

const messages = defineMessages({
  submit: {
    id: 'Submit',
    defaultMessage: 'Submit',
  },
  cancel: {
    id: 'Cancel',
    defaultMessage: 'Cancel',
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

interface SchemaFormBlockEditProps {
  data: SchemaFormBlockData;
  block: string;
  selected: boolean;
  onChangeBlock: (block: string, data: SchemaFormBlockData) => void;
  [key: string]: any;
}

const SchemaFormBlockEdit: React.FC<SchemaFormBlockEditProps> = (props) => {
  const { data, block, selected, onChangeBlock } = props;
  const intl = useIntl();

  const submitLabel = data.submit_label || intl.formatMessage(messages.submit);
  const cancelLabel = data.cancel_label || intl.formatMessage(messages.cancel);

  const schemaFormConfig = config.blocks.blocksConfig.schemaForm;
  const dummyHandler = () => {};

  return (
    <>
      {data.title && <h2>{data.title}</h2>}
      {data.description && <p>{data.description}</p>}
      <Form
        schema={{
          fieldsets: [
            {
              behavior: 'plone',
              fields: ['schema'],
              id: 'default',
              title: 'Default',
            },
          ],
          properties: {
            schema: {
              description: '',
              factory: 'Text',
              title: 'Schema',
              type: 'string',
              widget: 'schema',
              default: defaultEmptyData,
              filterFactory: schemaFormConfig.filterFactory,
              additionalFactory: schemaFormConfig.additionalFactory,
              allowEditId: true,
              allowEditQueryParameter: true,
              allowEditPlaceholder: true,
              widgets: schemaFormConfig.widgets,
            },
          },
          required: [],
          title: 'Form',
          type: 'object',
        }}
        component={schemaFormConfig.component}
        buttonComponent={schemaFormConfig.buttonComponent}
        formData={
          isEmpty(data.schema)
            ? { schema: defaultEmptyData }
            : { schema: stripRequiredProperty(data.schema) }
        }
        onChangeFormData={(formData: { schema: JSONSchema }) => {
          onChangeBlock(block, {
            ...data,
            schema: formData.schema,
          });
        }}
        onSubmit={dummyHandler}
        onCancel={data.show_cancel ? dummyHandler : null}
        submitLabel={submitLabel}
        cancelLabel={cancelLabel}
        textButtons={true}
      />

      <SidebarPortal selected={selected}>
        <SchemaFormBlockDataForm {...props} />
      </SidebarPortal>
    </>
  );
};

export default withBlockExtensions(SchemaFormBlockEdit);
