from email.message import EmailMessage
from email.utils import formataddr
from plone import api
from plone.base.interfaces.controlpanel import IMailSchema
from plone.formblock import _
from plone.formblock.interfaces import FormSubmissionContext
from plone.formblock.interfaces import IFormSubmissionProcessor
from plone.formblock.utils.email import create_message
from plone.registry.registry import Registry
from Products.MailHost.MailHost import MailHost
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer

import re


def is_mailhost_configured() -> bool:
    smtp_host = api.portal.get_registry_record("plone.smtp_host")
    email_from_address = api.portal.get_registry_record("plone.email_from_address")
    return bool(smtp_host and email_from_address)


def substitute_variables(
    value: str, context: dict | None = None, form_data: dict | None = None
) -> str:
    if context is None and form_data is not None:
        context = form_data
    elif context is None:
        context = {}

    def replace(match):
        name = match.group(1)
        return context.get(name, "")

    pattern = r"\$\{([^}]+)\}"
    return re.sub(pattern, replace, value)


@implementer(IFormSubmissionProcessor)
@adapter(FormSubmissionContext)
class EmailFormProcessor:
    """Sends an email with submitted form data"""

    order = 1
    templates: dict
    charset: str

    def __init__(self, context: FormSubmissionContext):
        self.context = context.context
        self.request = context.request
        self.block = context.block
        self.form_data = context.form_data
        self.records = context.get_records()
        self.attachments = context.get_attachments()
        self.portal_transforms = api.portal.get_tool(name="portal_transforms")
        self.templates: dict = (
            api.portal.get_registry_record("schemaform.mail_templates") or {}
        )

        registry: Registry = api.portal.get_tool("portal_registry")
        self.mail_settings = registry.forInterface(IMailSchema, prefix="plone")
        self.charset: str = registry.get("plone.email_charset", "utf-8")

    def _body_as_plain_text(self, html: str) -> str:
        tool = self.portal_transforms
        text = tool.convertTo("text/plain", html, mimetype="text/html").getData()
        return text.strip()

    def get_sender(self) -> str:
        sender = self.block.get("sender", "")
        sender = (
            substitute_variables(sender, context=self.form_data)
            or self.mail_settings.email_from_address
        )

        sender_name = self.block.get("sender_name", "")
        sender_name = (
            substitute_variables(sender_name, context=self.form_data)
            or self.mail_settings.email_from_name
        )

        return formataddr((sender_name, sender))

    def get_subject(self) -> str:
        subject = self.block.get("subject")
        schema_properties = self.block.get("schema", {}).get("properties", {})
        if not subject:
            if "subject" in schema_properties:
                subject = "${subject}"
            else:
                subject = self.block.get("title") or "Form Submission"
        subject = substitute_variables(subject, context=self.form_data)
        return subject

    def get_value(self, field_id, default=None):
        return self.form_data.get(field_id, default)

    def get_bcc(self) -> str:
        bcc: str = self.block.get("bcc", "")
        bcc = substitute_variables(bcc, context=self.form_data)
        return bcc or ""

    def get_confirmation_recipients(self) -> str:
        confirmation_recipients = self.block.get("confirmation_recipients", "")
        confirmation_recipients = substitute_variables(
            confirmation_recipients, context=self.form_data
        )
        return confirmation_recipients

    def prepare_message(self, admin=False):  # noqa: C901
        template_name = self.block.get("email_template", "default")
        admin_info = self.block.get("admin_info", "")
        properties = self.block.get("schema").get("properties")
        template = self.templates.get(template_name, "")
        plone = getMultiAdapter((self.context, self.request), name="plone")
        template_vars = {
            "mail_header": substitute_variables(
                self.block.get("mail_header", {}).get("data", ""),
                context=self.form_data,
            ),
            "mail_footer": substitute_variables(
                self.block.get("mail_footer", {}).get("data", ""),
                context=self.form_data,
            ),
        }
        form_fields = ""
        if admin:
            form_fields += admin_info.replace("\n", "<br/>") + "<br/><br/>"

        def format_property(factory, value):
            if factory == "label_boolean_field" or factory == "termsAccepted":
                if value == True:  # noqa: E712
                    return self.context.translate(
                        _("Yes"),
                        context=self.request,
                    )
                else:
                    return self.context.translate(
                        _("No"),
                        context=self.request,
                    )
            elif factory == "checkbox_group":
                if isinstance(value, list):
                    return "<br/>".join(value)
                else:
                    return str(value)
            elif factory == "label_date_field":
                return plone.toLocalizedTime(value)
            elif factory == "label_datetime_field":
                return plone.toLocalizedTime(value, True)
            else:
                return str(value)

        form_fields += "<table>\n"
        for record in self.records:
            factory = properties[record["field_id"]].get("factory", "")
            value = format_property(factory, record["value"])
            template_vars[record["field_id"]] = value

            if factory == "hidden" and not admin:
                continue
            if record["field_id"] == "captchaWidget":
                continue

            form_fields += (
                f'<tr><th align="left">{record["label"]}</th><td>{value}</td></tr>'
            )
        form_fields += "\n</table>\n"
        template_vars["form_fields"] = form_fields
        message = substitute_variables(template, template_vars)
        return message

    def send_mail(self, msg: EmailMessage, charset: str) -> None:
        host: MailHost = api.portal.get_tool(name="MailHost")
        # we set immediate=True because we need to catch exceptions.
        # by default (False) exceptions are handled by MailHost and we can't catch them.
        host.send(msg, charset=charset, immediate=True)

    def _prepare_msg_admin(self, mfrom: str, mto: str, subject: str) -> EmailMessage:
        body = self.prepare_message(True)
        body_text = self._body_as_plain_text(body)

        headers = {}
        headers_to_forward = self.block.get("httpHeaders", [])
        for header in headers_to_forward:
            header_value = self.request.get(header)
            if header_value:
                headers[header] = header_value

        return create_message(
            mfrom=mfrom,
            mto=mto,
            subject=subject,
            body=body,
            body_txt=body_text,
            reply_to=mfrom,
            bcc=self.get_bcc(),
            headers=headers,
            attachments=self.attachments,
        )

    def _prepare_msg_confirmation(
        self, mfrom: str, mto: str, subject: str
    ) -> EmailMessage:
        body = self.prepare_message()
        body_text = self._body_as_plain_text(body)

        attachments = {}
        if self.block.get("fixed_attachment"):
            attachments["fixed_attachment"] = self.block["fixed_attachment"]

        return create_message(
            mfrom=mfrom,
            mto=mto,
            subject=subject,
            body=body,
            body_txt=body_text,
            reply_to="",
            headers={},
            attachments=attachments,
        )

    def __call__(self) -> None:
        queued: list[EmailMessage] = []
        send_to_admin = bool(self.block.get("send"))
        send_confirmation = bool(self.block.get("send_confirmation"))
        if not send_to_admin and not send_confirmation:
            return

        if not is_mailhost_configured():
            raise BadRequest("MailHost is not configured.")

        subject = self.get_subject()
        mfrom = self.get_sender()

        if send_to_admin:
            mto = self.block.get("recipients", self.mail_settings.email_from_address)
            msg = self._prepare_msg_admin(mfrom, mto, subject)
            queued.append(msg)

        if send_confirmation and (mto := self.get_confirmation_recipients()):
            msg = self._prepare_msg_confirmation(mfrom, mto, subject)
            queued.append(msg)

        for msg in queued:
            self.send_mail(msg=msg, charset=self.charset)
