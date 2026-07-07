from plone.dexterity.content import DexterityContent
from plone.schema import JSONField
from typing import Any
from typing import TypedDict
from zope import schema
from zope.interface import Attribute
from zope.interface import Interface
from zope.publisher.http import HTTPRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import dataclasses


class IBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFormDataStore(Interface):
    def add(data):
        """
        Add data to the store

        @return: record id
        """

    def length():
        """
        @return: number of items stored into store
        """

    def search(query):
        """
        @return: items that match query
        """


class ICaptchaSupport(Interface):
    def __init__(context, request):
        """Initialize adapter"""

    def is_enabled():
        """Captcha method enabled
        @return: True if the method is enabled/configured
        """

    def verify(data):
        """Verify the captcha
        @return: True if verified, Raise exception otherwise
        """


class FormSchema(TypedDict):
    """A JSON Schema definition for a form block."""

    properties: dict[str, dict]
    fieldsets: list[dict]
    required: list[str]


class RichTextField(TypedDict):
    data: str


class SchemaFormBlock(TypedDict):
    """A form block schema definition."""

    schema: FormSchema
    title: str
    description: str
    submit_label: str
    show_cancel: bool
    cancel_label: str
    forward_user_to: str
    success: str
    thankyou: str
    captcha: str
    send: bool
    recipients: str
    bcc: str
    admin_info: str
    sender: str
    sender_name: str
    subject: str
    mail_header: RichTextField
    mail_footer: RichTextField
    store: bool
    data_wipe: int
    send_confirmation: bool
    confirmation_recipients: str
    fixed_attachment: Any
    mail_template: str


@dataclasses.dataclass
class AddressesFromBlock:
    """Addresses extracted from a form block, with variable substitution."""

    sender: str
    admin_recipients: str
    confirmation_recipients: str
    bcc: str


@dataclasses.dataclass
class FormSubmissionContext:
    context: DexterityContent
    block: SchemaFormBlock
    form_data: dict
    request: HTTPRequest
    addresses: AddressesFromBlock

    def get_records(self) -> list:
        """
        Return field id, value, and label.

        Skips file upload fields.
        """
        records = []
        for k, v in self.form_data.items():
            field = self.block["schema"]["properties"].get(k, {})
            if field.get("type") == "object":
                continue
            records.append({
                "field_id": k,
                "value": v,
                "label": field.get("title", k),
            })
        return records

    def get_attachments(self) -> dict:
        attachments = {}
        for k, v in self.form_data.items():
            field = self.block["schema"]["properties"].get(k, {})
            if field.get("factory") == "File Upload":
                attachments[k] = v
        return attachments


class IPostEvent(Interface):
    """An event triggered when a form is submitted."""

    context: FormSubmissionContext


class IFormSubmissionProcessor(Interface):
    """Subscriber which processes form data when it is submitted"""

    order: int = Attribute("Processors with the lowest order are processed first")

    def __init__(context: FormSubmissionContext):
        pass

    def __call__():
        """Process the data."""


DEFAULT_TEMPLATE = """
${mail_header}
<hr />
${form_fields}
<hr />
${mail_footer}
"""


class IFormSettings(Interface):
    mail_templates = schema.Dict(
        title="Email templates (Deprecated)",
        key_type=schema.TextLine(),
        value_type=schema.Text(),
        default={},
    )
    mail_templates_json = JSONField(
        title="Email templates",
        default={"default": DEFAULT_TEMPLATE},
    )
