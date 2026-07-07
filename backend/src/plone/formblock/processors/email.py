from email.message import EmailMessage
from plone import api
from plone.formblock.interfaces import FormSubmissionContext
from plone.formblock.interfaces import IFormSubmissionProcessor
from plone.formblock.interfaces import SchemaFormBlock
from plone.formblock.utils import email as utils
from Products.MailHost.MailHost import MailHost
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer


def template_vars_from_block(block: SchemaFormBlock, form_data: dict) -> dict:
    """Extract template variables from a form block.

    Substituting variables if necessary.
    """
    attrs = ("mail_header", "mail_footer")
    template_vars = {}
    for attr in attrs:
        value = block.get(attr, {}).get("data", "")
        template_vars[attr] = utils.substitute_variables(value, context=form_data)
    return template_vars


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
        self.addresses = context.addresses
        self.block = context.block
        self.template = utils.get_template_from_block(self.block)
        self.form_data = context.form_data
        self.records = context.get_records()
        self.attachments = context.get_attachments()
        self.portal_transforms = api.portal.get_tool(name="portal_transforms")

    def _body_as_plain_text(self, html: str) -> str:
        tool = self.portal_transforms
        text = tool.convertTo("text/plain", html, mimetype="text/html").getData()
        return text.strip()

    def get_subject(self) -> str:
        subject = self.block.get("subject")
        schema_properties = self.block.get("schema", {}).get("properties", {})
        if not subject:
            if "subject" in schema_properties:
                subject = "${subject}"
            else:
                subject = self.block.get("title") or "Form Submission"
        subject = utils.substitute_variables(subject, context=self.form_data)
        return subject

    def get_value(self, field_id, default=None):
        return self.form_data.get(field_id, default)

    def prepare_message(self, admin: bool = False) -> str:
        block = self.block
        form_data = self.form_data
        template = self.template
        template_vars = template_vars_from_block(block, form_data)
        admin_info = block.get("admin_info", "")
        properties = block.get("schema", {}).get("properties")
        form_fields = admin_info.replace("\n", "<br/>") + "<br/><br/>" if admin else ""
        form_fields += "<table>\n"
        for record in self.records:
            factory = properties[record["field_id"]].get("factory", "")
            value = utils.format_property(factory, record["value"])
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
        message = utils.substitute_variables(template, template_vars)
        return message

    def send_mail(self, msg: EmailMessage, charset: str) -> None:
        host: MailHost = api.portal.get_tool(name="MailHost")
        # we set immediate=True because we need to catch exceptions.
        # by default (False) exceptions are handled by MailHost and we can't catch them.
        host.send(msg, charset=charset, immediate=True)

    def _prepare_msg_admin(
        self, mfrom: str, mto: str, subject: str, bcc: str
    ) -> EmailMessage:
        body = self.prepare_message(True)
        body_text = self._body_as_plain_text(body)

        headers = {}
        headers_to_forward = self.block.get("httpHeaders", [])
        for header in headers_to_forward:
            header_value = self.request.get(header)
            if header_value:
                headers[header] = header_value

        return utils.create_message(
            mfrom=mfrom,
            mto=mto,
            subject=subject,
            body=body,
            body_txt=body_text,
            reply_to=mfrom,
            bcc=bcc,
            headers=headers,
            attachments=self.attachments,
        )

    def _prepare_msg_confirmation(
        self, mfrom: str, mto: str, subject: str, bcc: str = ""
    ) -> EmailMessage:
        body = self.prepare_message()
        body_text = self._body_as_plain_text(body)

        attachments = {}
        if self.block.get("fixed_attachment"):
            attachments["fixed_attachment"] = self.block["fixed_attachment"]

        return utils.create_message(
            mfrom=mfrom,
            mto=mto,
            subject=subject,
            body=body,
            body_txt=body_text,
            reply_to="",
            bcc=bcc,
            headers={},
            attachments=attachments,
        )

    def __call__(self) -> None:
        queued: list[EmailMessage] = []
        block = self.block
        addresses = self.addresses
        send_to_admin = bool(block.get("send"))
        send_confirmation = bool(block.get("send_confirmation"))
        if not send_to_admin and not send_confirmation:
            return

        if not utils.is_mailhost_configured():
            raise BadRequest("MailHost is not configured.")

        subject = self.get_subject()
        mfrom = addresses.sender

        if send_to_admin:
            mto = addresses.admin_recipients
            bcc = addresses.bcc
            msg = self._prepare_msg_admin(mfrom, mto, subject, bcc)
            queued.append(msg)

        if send_confirmation and (mto := addresses.confirmation_recipients.strip()):
            msg = self._prepare_msg_confirmation(mfrom, mto, subject)
            queued.append(msg)

        charset = api.portal.get_registry_record("plone.email_charset", default="utf-8")
        for msg in queued:
            self.send_mail(msg=msg, charset=charset)
