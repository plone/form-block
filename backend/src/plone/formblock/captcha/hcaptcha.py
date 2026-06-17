from . import ExternalCaptchaSupport
from plone.formblock import _
from plone.formwidget.hcaptcha.interfaces import IHCaptchaSettings
from plone.formwidget.hcaptcha.nohcaptcha import submit
from zExceptions import BadRequest
from zope.i18n import translate


class HCaptchaSupport(ExternalCaptchaSupport):
    name = _("HCaptcha")
    interface = IHCaptchaSettings
    _registry_keys = ("public_key", "private_key")
    public_key: str = ""
    private_key: str = ""

    def __init__(self, context, request):
        super().__init__(context, request)
        self._get_registry_settings()

    def isEnabled(self) -> bool:
        return bool(self.public_key and self.private_key)

    def serialize(self):
        if not self.public_key:
            raise ValueError(
                "No hcaptcha public key configured. Go to "
                "path/to/site/@@hcaptcha-settings to configure."
            )
        return {
            "provider": "hcaptcha",
            "public_key": self.public_key,
        }

    def verify(self, form_data: dict | None = None):
        if not self.private_key:
            raise ValueError(
                "No hcaptcha private key configured. Go to "
                "path/to/site/@@hcaptcha-settings to configure."
            )
        token = (form_data.get("captcha", {}) if form_data else {}).get("token")
        value = token or (form_data.get("data", {}) if form_data else {}).get(
            "captchaWidget"
        )
        if not value:
            raise BadRequest(
                translate(
                    _("No captcha token provided."),
                    context=self.request,
                )
            )
        res = submit(value, self.private_key)
        if not res.is_valid:
            raise BadRequest(
                translate(
                    _("The code you entered was wrong, please enter the new one."),
                    context=self.request,
                )
            )


class HCaptchaInvisibleSupport(HCaptchaSupport):
    name = _("HCaptcha Invisible")
