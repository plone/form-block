from . import CaptchaSupport
from collective.honeypot.config import HONEYPOT_FIELD
from collective.honeypot.utils import found_honeypot
from plone.formblock import _
from zExceptions import BadRequest
from zope.i18n import translate


class HoneypotSupport(CaptchaSupport):
    name = _("Honeypot Support")

    def isEnabled(self) -> bool:
        """Honeypot is enabled with env vars."""
        return True

    def serialize(self) -> dict:
        if not HONEYPOT_FIELD:
            # no field is set, so we only want to log.
            return {}
        return {"id": HONEYPOT_FIELD}

    def verify(self, form_data: dict | None = None):
        form_data = form_data or {}
        data = form_data.get("data", {}) or {}
        request = self.request
        msg = translate(
            _("honeypot_error", default="Error submitting form."),
            context=request,
        )
        if found_honeypot(data, required=False) or (HONEYPOT_FIELD in data):
            raise BadRequest(msg)
