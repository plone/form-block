from plone.dexterity.content import DexterityContent
from zope.publisher.http import HTTPRequest


class CaptchaSupport:
    context: DexterityContent
    request: HTTPRequest

    def __init__(self, context: DexterityContent, request: HTTPRequest):
        self.context = context
        self.request = request

    def isEnabled(self) -> bool:
        return True

    def verify(self, form_data: dict | None = None):
        """Verify the captcha."""
        raise NotImplementedError

    def _get_remote_addr(self) -> str:
        remote_addr = self.request.get("REMOTE_ADDR", "") or ""
        x_forwarded_for: list = (
            self.request.get("HTTP_X_FORWARDED_FOR", "") or ""
        ).split(",")
        if x_forwarded_for and x_forwarded_for[0].strip():
            remote_addr = x_forwarded_for[0].strip() or remote_addr
        # Use IPv4 loopback address instead of IPv6
        if remote_addr == "::1":
            remote_addr = "127.0.0.1"
        return str(remote_addr)
