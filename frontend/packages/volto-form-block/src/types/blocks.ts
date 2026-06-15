import React from 'react';
import type { BlockConfigBase } from '@plone/types';

interface FactoryOption {
  value: string;
  label: string;
}

export interface SchemaFormConfig extends BlockConfigBase {
  captchaProvidersVocabulary: string;
  mailTemplatesVocabulary: string;
  disableEnter: boolean;
  innerWidgets?: Record<string, React.ComponentType<any>>;
  widgets: Record<string, any> | null;
  component: React.ComponentType<any> | null;
  buttonComponent: React.ComponentType<any> | null;
  filterFactory: string[];
  additionalFactory: FactoryOption[];
  filterFactorySend: string[];
  defaultSender: string;
  defaultSenderName: string;
  security?: {
    addPermission: string[];
    view: string[];
  };
}
