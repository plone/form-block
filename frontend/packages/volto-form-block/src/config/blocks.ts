import type { ConfigType } from '@plone/registry';
import type { SchemaFormConfig } from '@plone/volto-form-block/types/blocks';
import schemaFormBlock from '@plone/volto-form-block/components/Blocks/SchemaForm';

declare module '@plone/types' {
  export interface BlocksConfigData {
    schemaForm: SchemaFormConfig;
  }
}

function installSchemaFormBlock(config: ConfigType) {
  config.blocks.blocksConfig.schemaForm = schemaFormBlock;
  return config;
}

export default function install(config: ConfigType) {
  installSchemaFormBlock(config);
  return config;
}
