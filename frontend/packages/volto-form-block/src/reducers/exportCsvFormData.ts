import { EXPORT_CSV_FORMDATA } from '@plone/volto-form-block/constants/ActionTypes';

interface ActionState {
  loaded: boolean;
  loading: boolean;
  error: string | null;
  result?: string | null;
  subrequests: Record<string, ActionState>;
}

interface ExportCsvFormDataAction {
  type: string;
  filename?: string;
  result?: string;
  error?: {
    response: {
      error: string;
    };
  };
}

const initialState: ActionState = {
  error: null,
  loaded: false,
  loading: false,
  subrequests: {},
};

function download(filename: string, text: string) {
  var element = document.createElement('a');
  element.setAttribute(
    'href',
    'data:text/comma-separated-values;charset=utf-8,' +
      encodeURIComponent(text),
  );
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

/**
 * exportCsvFormData reducer.
 * @function exportCsvFormData
 * @param {Object} state Current state.
 * @param {Object} action Action to be handled.
 * @returns {Object} New state.
 */
export const exportCsvFormData = (
  state: ActionState = initialState,
  action: ExportCsvFormDataAction,
) => {
  switch (action.type) {
    case `${EXPORT_CSV_FORMDATA}_PENDING`:
      return {
        ...state,
        error: null,
        result: null,
        loaded: false,
        loading: true,
      };
    case `${EXPORT_CSV_FORMDATA}_SUCCESS`:
      download(action.filename ?? `export-form.csv`, action.result ?? '');

      return {
        ...state,
        error: null,
        result: action.result,
        loaded: true,
        loading: false,
      };
    case `${EXPORT_CSV_FORMDATA}_FAIL`:
      return {
        ...state,
        error: action.error,
        result: null,
        loaded: false,
        loading: false,
      };
    default:
      return state;
  }
};
