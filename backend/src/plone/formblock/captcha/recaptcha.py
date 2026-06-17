from . import ExternalCaptchaSupport
from plone.formblock import _
from plone.formwidget.recaptcha.interfaces import IReCaptchaSettings
from plone.formwidget.recaptcha.norecaptcha import submit
from plone.formwidget.recaptcha.norecaptcha import submit_v3
from zExceptions import BadRequest
from zope.i18n import translate


class RecaptchaSupport(ExternalCaptchaSupport):
    name = _("Google ReCaptcha")
    interface = IReCaptchaSettings
    _registry_keys = ("public_key", "private_key", "api_version")
    public_key: str = ""
    private_key: str = ""
    api_version: str = "v3"
    use_recaptcha_net: bool = True

    def __init__(self, context, request):
        super().__init__(context, request)
        self._get_registry_settings()

    def _format_error_code(self, error_code: str | list[str] | None) -> str:
        message: str = ""
        if isinstance(error_code, str):
            message = error_code
        elif isinstance(error_code, list) and error_code:
            message = ", ".join(error_code)
        return message or "unknown error"

    def isEnabled(self) -> bool:
        return bool(self.public_key and self.private_key)

    def serialize(self):
        if not self.public_key:
            raise ValueError(
                "No recaptcha public key configured. Go to "
                "path/to/site/@@recaptcha-settings to configure."
            )
        return {
            "provider": "recaptcha",
            "public_key": self.public_key,
            "use_recaptcha_net": self.use_recaptcha_net,
        }

    def verify(self, form_data: dict | None = None):

        if not self.private_key:
            raise ValueError(
                "No recaptcha private key configured. Go to "
                "path/to/site/@@recaptcha-settings to configure."
            )
        func = submit_v3 if self.api_version == "v3" else submit
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
        remote_addr = self._get_remote_addr()
        verify_server = (
            "www.recaptcha.net" if self.use_recaptcha_net else "www.google.com"
        )
        res = func(value, self.private_key, remote_addr, verify_server=verify_server)
        if not res.is_valid:
            error_code = self._format_error_code(res.error_code)
            raise BadRequest(
                "{error} ({code})".format(
                    error=translate(
                        _("The code you entered was wrong, please enter the new one."),
                        context=self.request,
                    ),
                    code=error_code,
                )
            )
