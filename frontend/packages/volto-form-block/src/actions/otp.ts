import { RESET_OTP } from '@plone/volto-form-block/constants/ActionTypes';
import { SEND_OTP } from '@plone/volto-form-block/constants/ActionTypes';
/**
 * sendOTP action
 * @module actions/otp
 */

export function sendOTP(path: string, block_id: string, email: string) {
  return {
    type: SEND_OTP,
    subrequest: `otp_${block_id}_${email}`,
    request: {
      op: 'post',
      path: `${path}/@validate-email-address`,
      data: {
        email,
        uid: block_id,
      },
    },
  };
}

/**
 * resetOTP action
 * @module actions/otp
 */

export function resetOTP(block_id: string) {
  return {
    type: RESET_OTP,
    block_id,
  };
}
