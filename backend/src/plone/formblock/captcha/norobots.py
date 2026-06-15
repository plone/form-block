from . import CaptchaSupport
from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings
from plone import api
from plone.formblock import _
from zExceptions import BadRequest
from zope.i18n import translate


class NoRobotsSupport(CaptchaSupport):
    name = _("NoRobots ReCaptcha Support")

    def __init__(self, context, request):
        super().__init__(context, request)
        try:
            questions = api.portal.get_registry_record(
                interface=INorobotsWidgetSettings, name="questions", default=()
            )
        except KeyError:
            questions = ()
        self.questions = questions

    def isEnabled(self) -> bool:
        return bool(self.questions)

    def serialize(self):
        if not self.questions:
            raise ValueError(
                "No recaptcha public key configured. Go to "
                "path/to/site/@@norobots-controlpanel to configure."
            )

        view = api.content.get_view(
            context=self.context, request=self.request, name="norobots"
        )

        question = view.get_question()
        question.update({"provider": "norobots-captcha"})
        return question

    def verify(self, form_data: dict | None = None):
        if not self.questions:
            raise ValueError(
                "No question configured. Go to "
                "path/to/site/@@norobots-controlpanel to configure."
            )

        if not form_data:
            raise BadRequest(
                translate(
                    _("No captcha token provided."),
                    context=self.request,
                )
            )

        data = form_data.get("data", {}) or {}
        value = data.get("captchaWidget")
        if not value:
            raise BadRequest(
                translate(
                    _("No captcha token provided."),
                    context=self.request,
                )
            )
        captcha_props = (form_data.get("captcha", {}) or {}).get("props", {})
        view = api.content.get_view(
            context=self.context, request=self.request, name="norobots"
        )
        id_ = captcha_props.get("id")
        id_check = captcha_props.get("id_check")
        if not view.verify(input=value, question_id=id_, id_check=id_check):
            raise BadRequest(
                translate(
                    _("The code you entered was wrong, please enter the new one."),
                    context=self.request,
                )
            )
