import type { ConfigType } from '@plone/registry';
import loadable from '@loadable/component';

export default function install(config: ConfigType) {
  config.settings.loadables = {
    ...(config.settings.loadables as Record<string, unknown>),
    HCaptcha: loadable(() => import('@hcaptcha/react-hcaptcha')),
    GoogleReCaptcha: loadable.lib(() => import('react-google-recaptcha-v3')),
    ReactTable: loadable.lib(() => import('@tanstack/react-table')),
  };
  return config;
}
