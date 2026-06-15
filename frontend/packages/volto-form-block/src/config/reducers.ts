import type { ConfigType } from '@plone/registry';
import { submitForm } from '@plone/volto-form-block/reducers/submitForm';
import { getFormData } from '@plone/volto-form-block/reducers/getFormData';
import { exportCsvFormData } from '@plone/volto-form-block/reducers/exportCsvFormData';
import { clearFormData } from '@plone/volto-form-block/reducers/clearFormData';
import { sendOTP } from '@plone/volto-form-block/reducers/sendOTP';

export default function install(config: ConfigType) {
  config.addonReducers = {
    ...config.addonReducers,
    submitForm,
    formData: getFormData,
    exportCsvFormData,
    clearFormData,
    sendOTP,
  };
  return config;
}
