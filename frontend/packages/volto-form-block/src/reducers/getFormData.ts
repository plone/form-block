import { GET_FORM_DATA } from '@plone/volto-form-block/constants/ActionTypes';

interface ActionState {
  loaded: boolean;
  loading: boolean;
  error: string | null;
  result?: Record<string, unknown> | null;
  subrequests: Record<string, ActionState>;
}

interface GetFormDataAction {
  type: string;
  result?: Record<string, unknown>;
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

/**
 * getFormData reducer.
 * @function getFormData
 * @param {Object} state Current state.
 * @param {Object} action Action to be handled.
 * @returns {Object} New state.
 */
export const getFormData = (
  state: ActionState = initialState,
  action: GetFormDataAction,
) => {
  switch (action.type) {
    case `${GET_FORM_DATA}_PENDING`:
      return {
        ...state,
        error: null,
        loaded: false,
        loading: true,
        result: null,
      };
    case `${GET_FORM_DATA}_SUCCESS`:
      return {
        ...state,
        error: null,
        loaded: true,
        result: action.result,
        loading: false,
      };
    case `${GET_FORM_DATA}_FAIL`:
      return {
        ...state,
        error: action.error,
        result: null,
        loaded: true,
        loading: false,
      };
    default:
      return state;
  }
};
