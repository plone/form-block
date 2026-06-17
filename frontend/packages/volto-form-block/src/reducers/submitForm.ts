import { SUBMIT_FORM_ACTION } from '@plone/volto-form-block/constants/ActionTypes';

interface ActionState {
  loaded: boolean;
  loading: boolean;
  error: string | null;
  result?: Record<string, unknown> | null;
  subrequests: Record<string, ActionState>;
}

interface SubmitFormAction {
  type: string;
  subrequest?: string;
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
 * submitForm reducer.
 * @function submitForm
 * @param {Object} state Current state.
 * @param {Object} action Action to be handled.
 * @returns {Object} New state.
 */
export const submitForm = (
  state: ActionState = initialState,
  action: SubmitFormAction,
) => {
  switch (action.type) {
    case `${SUBMIT_FORM_ACTION}_PENDING`:
      return action.subrequest
        ? {
            ...state,
            subrequests: {
              ...state.subrequests,
              [action.subrequest]: {
                ...(state.subrequests[action.subrequest] || {
                  result: null,
                }),
                error: null,
                loaded: false,
                loading: true,
              },
            },
          }
        : {
            ...state,
            result: null,
            error: null,
            loading: true,
            loaded: false,
          };
    case `${SUBMIT_FORM_ACTION}_SUCCESS`:
      return action.subrequest
        ? {
            ...state,
            subrequests: {
              ...state.subrequests,
              [action.subrequest]: {
                ...(state.subrequests[action.subrequest] || {}),
                result: action.result,
                error: null,
                loaded: true,
                loading: false,
              },
            },
          }
        : {
            ...state,
            result: action.result,
            error: null,
            loaded: true,
            loading: false,
          };
    case `${SUBMIT_FORM_ACTION}_FAIL`:
      return action.subrequest
        ? {
            ...state,
            subrequests: {
              ...state.subrequests,
              [action.subrequest]: {
                ...(state.subrequests[action.subrequest] || {}),
                error: action.error,
                result: null,
                loading: false,
                loaded: false,
              },
            },
          }
        : {
            ...state,
            error: action.error,
            result: null,
            loading: false,
            loaded: false,
          };

    default:
      return state;
  }
};
