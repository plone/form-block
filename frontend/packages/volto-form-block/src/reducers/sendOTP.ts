import {
  SEND_OTP,
  RESET_OTP,
} from '@plone/volto-form-block/constants/ActionTypes';

interface ActionState {
  loaded: boolean;
  loading: boolean;
  error: string | null;
  subrequests: Record<string, ActionState>;
}

interface SendOTPAction {
  type: string;
  subrequest?: string;
  block_id?: string;
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
 * sendOTP reducer.
 * @function sendOTP
 * @param {Object} state Current state.
 * @param {Object} action Action to be handled.
 * @returns {Object} New state.
 */
export const sendOTP = (
  state: ActionState = initialState,
  action: SendOTPAction,
) => {
  switch (action.type) {
    case `${SEND_OTP}_PENDING`:
      return action.subrequest
        ? {
            ...state,
            subrequests: {
              ...state.subrequests,
              [action.subrequest]: {
                ...(state.subrequests[action.subrequest] || {
                  items: [],
                  total: 0,
                  batching: {},
                }),
                error: null,
                loaded: false,
                loading: true,
              },
            },
          }
        : {
            ...state,
            error: null,
            loading: true,
            loaded: false,
          };
    case `${SEND_OTP}_SUCCESS`:
      return action.subrequest
        ? {
            ...state,
            subrequests: {
              ...state.subrequests,
              [action.subrequest]: {
                ...(state.subrequests[action.subrequest] || {}),
                error: null,
                loaded: true,
                loading: false,
              },
            },
          }
        : {
            ...state,
            error: null,
            loaded: true,
            loading: false,
          };
    case `${SEND_OTP}_FAIL`:
      return action.subrequest
        ? {
            ...state,
            subrequests: {
              ...state.subrequests,
              [action.subrequest]: {
                ...(state.subrequests[action.subrequest] || {}),
                error: action.error,
                loading: false,
                loaded: false,
              },
            },
          }
        : {
            ...state,
            error: action.error,
            loading: false,
            loaded: false,
          };
    case RESET_OTP:
      let new_subrequests = { ...state.subrequests };

      if (action.block_id) {
        Object.keys(new_subrequests)
          .filter((k) => k.indexOf('otp_' + action.block_id) === 0)
          .forEach((k) => {
            delete new_subrequests[k];
          });
      }
      return action.block_id
        ? {
            ...state,
            subrequests: new_subrequests,
          }
        : {
            ...state,
            error: null,
            loading: true,
            loaded: false,
          };
    default:
      return state;
  }
};
