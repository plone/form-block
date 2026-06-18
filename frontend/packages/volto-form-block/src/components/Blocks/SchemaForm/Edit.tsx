import React, { useState } from 'react';
import isEmpty from 'lodash/isEmpty';
import { defineMessages, useIntl } from 'react-intl';
import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';
import { Form } from '@plone/volto/components/manage/Form';
import { withBlockExtensions } from '@plone/volto/helpers/Extensions';
import config from '@plone/volto/registry';
import { stripRequiredProperty } from '@plone/volto-form-block/helpers/schema';
import SchemaFormBlockDataForm from '@plone/volto-form-block/components/Blocks/SchemaForm/Data';
import DataTable from '@plone/volto-form-block/components/DataTable/DataTable';
import type { SchemaFormBlockData } from '@plone/volto-form-block/components/Blocks/SchemaForm/Data';
import type { Content, JSONSchema } from '@plone/types';

const messages = defineMessages({
  submit: {
    id: 'Submit',
    defaultMessage: 'Submit',
  },
  cancel: {
    id: 'Cancel',
    defaultMessage: 'Cancel',
  },
  showForm: {
    id: 'Show Form',
    defaultMessage: 'Show Form',
  },
  showData: {
    id: 'Show Data',
    defaultMessage: 'Show Data',
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
  properties: Content;
  block: string;
  selected: boolean;
  onChangeBlock: (block: string, data: SchemaFormBlockData) => void;
  [key: string]: any;
}

const DataTableWrapper: React.FC<{
  data: SchemaFormBlockData;
  properties: Content;
  block: string;
}> = ({ data, properties, block }) => {
  return (
    <DataTable
      properties={properties}
      blockId={block}
      removeDataAfterDays={data.data_wipe}
    />
  );
};

const SchemaFormBlockEdit: React.FC<SchemaFormBlockEditProps> = (props) => {
  const { data, block, properties, selected, onChangeBlock } = props;
  const intl = useIntl();

  const submitLabel = data.submit_label || intl.formatMessage(messages.submit);
  const cancelLabel = data.cancel_label || intl.formatMessage(messages.cancel);
  const showFormLabel = intl.formatMessage(messages.showForm);
  const showDataLabel = intl.formatMessage(messages.showData);
  const schemaFormConfig = config.blocks.blocksConfig.schemaForm;
  const [showForm, setShowForm] = useState(true);
  const storeData = data.store || false;
  const dummyHandler = () => {};

  return (
    <>
      {storeData && (
        <button
          className="ui primary button"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? showDataLabel : showFormLabel}
        </button>
      )}
      {showForm ? (
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
        </>
      ) : (
        <DataTableWrapper data={data} properties={properties} block={block} />
      )}
      <SidebarPortal selected={selected}>
        <SchemaFormBlockDataForm {...props} />
      </SidebarPortal>
    </>
  );
};

export default withBlockExtensions(SchemaFormBlockEdit);
