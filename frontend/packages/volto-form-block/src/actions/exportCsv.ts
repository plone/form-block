/**
 * exportCsvFormData action
 * @module actions/exportCsv
 */
import { EXPORT_CSV_FORMDATA } from '@plone/volto-form-block/constants/ActionTypes';

export function exportCsvFormData(
  path: string = '',
  filename: string,
  block_id: string,
) {
  return {
    type: EXPORT_CSV_FORMDATA,
    filename: filename,
    request: {
      op: 'get',
      path: `${path}/@form-data-export${
        block_id ? '?block_id=' + block_id : ''
      }`,
    },
  };
}
