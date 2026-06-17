import React, { createRef, useRef } from 'react';
import FormFieldWrapper from '@plone/volto/components/manage/Widgets/FormFieldWrapper';
import { injectLazyLibs } from '@plone/volto/helpers/Loadable/Loadable';
import { defineMessages, useIntl } from 'react-intl';
import '@plone/volto-form-block/components/Widgets/HCaptchaWidget.css';

const messages = defineMessages({
  invisibleCaptcha: {
    id: 'HCaptchaInvisibleInfo',
    defaultMessage:
      'This site is protected by hCaptcha and its ' +
      '<a href="https://www.hcaptcha.com/privacy">Privacy Policy</a> and ' +
      '<a href="https://www.hcaptcha.com/terms">Terms of Service</a> apply.',
  },
});

type HCaptchaWidgetProps = {
  id: string;
  onChange: (id: string, value: string) => void;
  onEdit?: boolean;
  captcha_props: { provider: string; public_key: string; size?: string };
  HCaptcha: { default: React.ComponentType<any> };
};

const HCaptchaWidget = ({
  id,
  onChange,
  onEdit,
  captcha_props,
  HCaptcha: hcaptchalib,
}: HCaptchaWidgetProps) => {
  const captchaRef = createRef<any>();
  const HCaptchaComponent = hcaptchalib.default;
  const intl = useIntl();
  const sitekey = captcha_props.public_key;
  const size = captcha_props.size || 'normal';
  const captchaToken = useRef<string | null>(null);
  const onVerify = (token: string) => {
    captchaToken.current = token;
    onChange(id, token);
  };

  const onExpire = () => {
    captchaToken.current = null;
  };

  const onLoad = () => {
    captchaRef.current?.execute();
  };

  return onEdit ? (
    <></>
  ) : size === 'invisible' ? (
    <FormFieldWrapper
      id={id}
      label={''}
      title={''}
      required={false}
      error={''}
      className="hCaptchaWidget"
    >
      <HCaptchaComponent
        ref={captchaRef}
        sitekey={sitekey}
        onLoad={onLoad}
        onVerify={onVerify}
        onExpire={onExpire}
        size={size}
      />
      <div
        dangerouslySetInnerHTML={{
          __html: intl.formatMessage(messages.invisibleCaptcha),
        }}
      />
    </FormFieldWrapper>
  ) : (
    <FormFieldWrapper
      id={id}
      label={''}
      title={''}
      required={false}
      error={''}
      className="hCaptchaWidget"
    >
      <HCaptchaComponent
        ref={captchaRef}
        sitekey={sitekey}
        onLoad={onLoad}
        onVerify={onVerify}
        size={size}
      />
    </FormFieldWrapper>
  );
};

export default injectLazyLibs(['HCaptcha'])(HCaptchaWidget);
