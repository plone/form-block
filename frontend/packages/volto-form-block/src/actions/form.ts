import { CLEAR_FORM_DATA } from '@plone/volto-form-block/constants/ActionTypes';
import { GET_FORM_DATA } from '@plone/volto-form-block/constants/ActionTypes';
import { SUBMIT_FORM_ACTION } from '@plone/volto-form-block/constants/ActionTypes';
/**
 * clearFormData action
 * @module actions/form
 */

export function clearFormData(
  path: string = '',
  block_id: string = '',
  expired: boolean = false,
) {
  const payload = {
    expired,
    block_id,
  };
  return {
    type: CLEAR_FORM_DATA,
    request: {
      op: 'del',
      path: `${path}/@form-data-clear`,
      data: payload,
    },
  };
}

/**
 * getFormData action
 * @module actions/form
 */

export function getFormData(path: string = '', block_id: string = '') {
  return {
    type: GET_FORM_DATA,
    request: {
      op: 'get',
      path: `${path}/@form-data${block_id ? '?block_id=' + block_id : ''}`,
    },
  };
}

/**
 * submitForm action
 * @module actions/form
 */

export function submitForm(
  path: string = '',
  block_id: string,
  data: object,
  captcha: object,
) {
  return {
    type: SUBMIT_FORM_ACTION,
    subrequest: block_id,
    request: {
      op: 'post',
      path: `${path}/@schemaform-data`,
      data: {
        block_id,
        data,
        captcha,
      },
    },
  };
}
