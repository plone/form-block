from email import policy
from email.message import EmailMessage
from email.utils import formataddr
from plone import api
from plone.formblock import _
from plone.formblock.interfaces import AddressesFromBlock
from plone.formblock.interfaces import DEFAULT_TEMPLATE
from plone.formblock.interfaces import SchemaFormBlock
from zope.publisher.http import HTTPRequest

import codecs
import os
import re


CTE = os.environ.get("MAIL_CONTENT_TRANSFER_ENCODING", None)


def is_mailhost_configured() -> bool:
    """Check if MailHost is configured with SMTP host and email from address."""
    smtp_host = api.portal.get_registry_record("plone.smtp_host")
    email_from_address = api.portal.get_registry_record("plone.email_from_address")
    return bool(smtp_host and email_from_address)


def available_templates() -> dict[str, str]:
    """Return a dictionary of available email templates."""
    templates: dict[str, str] = api.portal.get_registry_record(
        "schemaform.mail_templates_json"
    )
    return templates or {}


def get_template_from_block(block: SchemaFormBlock) -> str:
    """Return the email template for the given template name."""
    templates: dict[str, str] = available_templates()
    template_name = block.get("mail_template", "default")
    return templates.get(template_name) or DEFAULT_TEMPLATE


def substitute_variables(
    value: str, context: dict | None = None, form_data: dict | None = None
) -> str:
    """Substitute variables in the form ${variable_name} with values from the context
    or form_data.
    """
    if context is None and form_data is not None:
        context = form_data
    elif context is None:
        context = {}

    def replace(match):
        name = match.group(1)
        return context.get(name, "")

    pattern = r"\$\{([^}]+)\}"
    return re.sub(pattern, replace, value)


def format_property(factory: str, value: str | bool | list | None) -> str:
    response = str(value)
    if factory == "label_boolean_field" or factory == "termsAccepted":
        response = (
            api.portal.translate(_("Yes"))
            if value is True
            else api.portal.translate(_("No"))
        )
    elif factory == "checkbox_group" and isinstance(value, list):
        response = "<br/>".join(value)
    elif factory in ("label_date_field", "label_datetime_field"):
        util = api.portal.get_tool("translation_service")
        response = util.toLocalizedTime(
            value, long_format=factory == "label_datetime_field"
        )
    return response


def addresses_from_block(block: SchemaFormBlock, form_data: dict) -> AddressesFromBlock:
    """Extract addresses from a form block, substituting variables if necessary."""
    default_addr: str = api.portal.get_registry_record("plone.email_from_address")
    default_name: str = api.portal.get_registry_record("plone.email_from_name")
    admin_recipients: str = block.get("recipients", default_addr)
    _sender = (
        substitute_variables(block.get("sender", ""), context=form_data) or default_addr
    )
    _sender_name = (
        substitute_variables(block.get("sender_name", ""), context=form_data)
        or default_name
    )
    sender: str = formataddr((_sender_name, _sender))
    bcc: str = substitute_variables(block.get("bcc", ""), context=form_data) or ""
    rcpts: str = substitute_variables(
        block.get("confirmation_recipients", ""), context=form_data
    )
    return AddressesFromBlock(
        sender=sender,
        admin_recipients=admin_recipients,
        confirmation_recipients=rcpts,
        bcc=bcc,
    )


def add_attachaments_to_msg(
    msg: EmailMessage, attachments: dict[str, dict | str]
) -> None:
    for value in attachments.values():
        content_type = "application/octet-stream"
        filename = None
        if isinstance(value, dict):
            file_data = value.get("data", "")
            if not file_data:
                continue
            content_type = value.get("content-type", content_type)
            filename = value.get("filename", filename)
            if isinstance(file_data, str):
                file_data = file_data.encode("utf-8")
            if "encoding" in value:
                file_data = codecs.decode(file_data, value["encoding"])
            if isinstance(file_data, str):
                file_data = file_data.encode("utf-8")
        else:
            file_data = value
        maintype, subtype = content_type.split("/")
        msg.add_attachment(
            file_data,
            maintype=maintype,
            subtype=subtype,
            filename=filename,
        )


def create_message(
    mfrom: str,
    mto: str,
    subject: str,
    body: str,
    body_txt: str,
    reply_to: str = "",
    bcc: str = "",
    headers: dict | None = None,
    attachments: dict[str, dict | str] | None = None,
) -> EmailMessage:
    msg = EmailMessage(policy=policy.SMTP)
    msg.set_content(body_txt, cte=CTE)
    msg.add_alternative(body, subtype="html", cte=CTE)
    msg["Subject"] = subject
    msg["From"] = mfrom
    msg["Reply-To"] = reply_to or mfrom
    msg["To"] = mto.replace(";", ",")
    if bcc:
        msg["Bcc"] = bcc.replace(";", ",")

    headers = headers or {}
    for header, value in headers.items():
        if value:
            msg[header] = value
    attachments = attachments or {}
    add_attachaments_to_msg(msg=msg, attachments=attachments)
    return msg


def request_headers_from_block(
    block: SchemaFormBlock, request: HTTPRequest
) -> dict[str, str]:
    """Extract HTTP headers from a form block and request.

    Substituting variables if necessary.
    """
    raw_http_headers: str = block.get("httpHeaders", "") or ""
    headers_to_forward: list[str] = [
        header.strip().upper()
        for header in raw_http_headers.splitlines()
        if header.strip()
    ]
    headers: dict[str, str] = {}
    for header in headers_to_forward:
        if header_value := request.getHeader(header):
            headers[header] = header_value
    return headers
