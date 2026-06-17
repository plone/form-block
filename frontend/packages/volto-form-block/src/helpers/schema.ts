/**
 * Schema helper.
 * @module helpers/schema
 */
import config from '@plone/volto/registry';
import isObject from 'lodash/isObject';
import type { JSONSchema } from '@plone/types';

/**
 * Strip required property
 * @function stripRequiredProperty
 * @param {Object} schema Schema.
 * @return {Object} Schema with required property stripped
 */
export function stripRequiredProperty(schema: JSONSchema): JSONSchema {
  if (!isObject(schema) || !isObject(schema.properties)) {
    return schema;
  }

  for (const field in schema.properties) {
    delete schema.properties[field].required;
  }

  return schema;
}

export function getInnerWidget(
  widgetName: string,
): React.ComponentType<any> | null {
  const schemaFormConfig = config.blocks.blocksConfig.schemaForm;
  if (!schemaFormConfig || !schemaFormConfig.innerWidgets) {
    return null;
  }
  return schemaFormConfig.innerWidgets[widgetName] || null;
}
