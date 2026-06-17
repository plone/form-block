import type { ConfigType } from '@plone/registry';
import HoneypotCaptchaWidget from '@plone/volto-form-block/components/Widgets/HoneypotCaptchaWidget';
import NorobotsCaptchaWidget from '@plone/volto-form-block/components/Widgets/NorobotsCaptchaWidget';
import GoogleReCaptchaWidget from '@plone/volto-form-block/components/Widgets/GoogleReCaptchaWidget';
import HCaptchaWidget from '@plone/volto-form-block/components/Widgets/HCaptchaWidget';

export default function install(config: ConfigType) {
  // Edit widgets
  config.registerWidget({
    key: 'widget',
    definition: { honeypot: HoneypotCaptchaWidget },
  });
  config.registerWidget({
    key: 'widget',
    definition: { 'norobots-captcha': NorobotsCaptchaWidget },
  });
  config.registerWidget({
    key: 'widget',
    definition: { recaptcha: GoogleReCaptchaWidget },
  });
  config.registerWidget({
    key: 'widget',
    definition: { hcaptcha: HCaptchaWidget },
  });

  return config;
}
