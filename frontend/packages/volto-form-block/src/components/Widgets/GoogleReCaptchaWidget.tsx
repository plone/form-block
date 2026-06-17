import React, { useEffect, useRef } from 'react';
import { injectLazyLibs } from '@plone/volto/helpers/Loadable/Loadable';
import { useIntl } from 'react-intl';

type ReCaptchaLib = {
  useGoogleReCaptcha: () => {
    executeRecaptcha?: (action?: string) => Promise<string>;
  };
  GoogleReCaptchaProvider: React.ComponentType<any>;
};

type GoogleReCaptchaWidgetProps = {
  id: string;
  captcha_props: { public_key: string; use_recaptcha_net?: boolean };
  onChange: (id: string, value: () => Promise<string>) => void;
  onEdit?: boolean;
  GoogleReCaptcha: ReCaptchaLib;
};

const ReCaptchaComponent = (props: GoogleReCaptchaWidgetProps) => {
  const { GoogleReCaptcha: recaptchalib, id, onChange } = props;
  const { useGoogleReCaptcha } = recaptchalib;
  const { executeRecaptcha } = useGoogleReCaptcha();

  // The reCAPTCHA script loads asynchronously, so `executeRecaptcha` is
  // undefined on the first renders. Keep the latest value in a ref so the
  // verify function stored on the form is never pinned to that initial
  // undefined (which made the token always resolve to an empty string).
  const executeRecaptchaRef = useRef(executeRecaptcha);
  useEffect(() => {
    executeRecaptchaRef.current = executeRecaptcha;
  }, [executeRecaptcha]);

  useEffect(() => {
    // View.tsx awaits this at submit time to mint a fresh reCAPTCHA v3 token
    // (tokens expire after ~2 min, so it must run on submit, not on mount).
    const verify = async () => {
      const execute = executeRecaptchaRef.current;
      if (!execute) {
        return '';
      }
      return await execute();
    };
    onChange(id, verify);
  }, [id, onChange]);

  return null;
};

const GoogleReCaptchaWidget = (props: GoogleReCaptchaWidgetProps) => {
  const intl = useIntl();

  const { onEdit, captcha_props, GoogleReCaptcha: recaptchalib } = props;
  const { GoogleReCaptchaProvider } = recaptchalib;
  return onEdit ? (
    <></>
  ) : (
    <div className="googleReCaptchaWidget">
      <GoogleReCaptchaProvider
        reCaptchaKey={captcha_props.public_key}
        language={intl.locale ?? 'en'}
        // Load the script from recaptcha.net instead of www.google.com, which
        // can be blocked (ERR_BLOCKED_BY_ORB, geo-redirects, some networks).
        // recaptcha.net is Google's official global alternate and works
        // everywhere. Override per form via `captcha_props.use_recaptcha_net`.
        useRecaptchaNet={captcha_props.use_recaptcha_net ?? true}
      >
        <ReCaptchaComponent {...props} />
      </GoogleReCaptchaProvider>
    </div>
  );
};

export default injectLazyLibs(['GoogleReCaptcha'])(GoogleReCaptchaWidget);
