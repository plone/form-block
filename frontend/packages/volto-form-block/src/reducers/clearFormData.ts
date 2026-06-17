import { CLEAR_FORM_DATA } from '@plone/volto-form-block/constants/ActionTypes';

interface ActionState {
  loaded: boolean;
  loading: boolean;
  error: string | null;
  subrequests: Record<string, ActionState>;
}

interface ClearFormDataAction {
  type: string;
  result?: Record<string, unknown>;
  error?: {
    response: {
      error: string;
    };
  };
}

const initialState: ActionState = {
  loaded: false,
  loading: false,
  error: null,
  subrequests: {},
};

/**
 * clearFormData reducer.
 * @function clearFormData
 * @param {Object} state Current state.
 * @param {Object} action Action to be handled.
 * @returns {Object} New state.
 */
export const clearFormData = (
  state: ActionState = initialState,
  action: ClearFormDataAction,
) => {
  switch (action.type) {
    case `${CLEAR_FORM_DATA}_PENDING`:
      return {
        ...state,
        error: null,
        loaded: false,
        loading: true,
      };
    case `${CLEAR_FORM_DATA}_SUCCESS`:
      return {
        ...state,
        error: null,
        loaded: true,
        loading: false,
      };
    case `${CLEAR_FORM_DATA}_FAIL`:
      return {
        ...state,
        error: action.error,
        loaded: false,
        loading: false,
      };
    default:
      return state;
  }
};
