from plone.formblock import _
from plone.formblock.events import PostEvent
from plone.formblock.interfaces import FormSubmissionContext
from plone.formblock.interfaces import ICaptchaSupport
from plone.formblock.interfaces import IFormSubmissionProcessor
from plone.formblock.restapi.services.base import BaseService
from plone.formblock.utils import fix_block_schema
from plone.formblock.utils import get_blocks
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from zExceptions import BadRequest
from zExceptions import HTTPServerError
from zope.component import getMultiAdapter
from zope.component import subscribers
from zope.event import notify
from zope.i18n import translate
from zope.interface import alsoProvides

import json
import jsonschema
import logging
import math
import os


logger = logging.getLogger(__name__)


class SubmitPost(BaseService):
    block: dict
    block_id: str
    form_data: dict

    def _run_handlers(self, form_submission_context):
        """Run all handlers subscribed to IFormSubmissionProcessor"""
        all_handlers = subscribers((form_submission_context,), IFormSubmissionProcessor)
        for handler in sorted(all_handlers, key=lambda h: h.order):
            try:
                handler()
            except BadRequest:
                raise
            except Exception as err:
                logger.exception(err)
                message = translate(
                    _(
                        "form_action_exception",
                        default="Unable to process form. "
                        "Please retry later or contact site administrator.",
                    ),
                    context=self.request,
                )
                raise HTTPServerError(message) from err

    def cleanup_data(self, schema: dict, form_data: dict) -> dict:
        """Ignore fields not defined in form schema"""
        if not isinstance(form_data, dict):
            raise BadRequest(
                translate(
                    _(
                        "invalid_form_data",
                        default="Invalid form data.",
                    ),
                    context=self.request,
                )
            )
        form_data = {
            k: v for k, v in form_data.items() if k in schema.get("properties", {})
        }
        return form_data

    def validate_form(self):
        """Check all required fields and parameters."""
        if not self.block_id:
            raise BadRequest(
                translate(
                    _("missing_blockid_label", default="Missing block_id"),
                    context=self.request,
                )
            )
        if not self.block:
            raise BadRequest(
                translate(
                    _(
                        "block_form_not_found_label",
                        default='Block with @type "schemaForm" and id "$block" not found in this context: $context',  # noqa: E501
                        mapping={
                            "block": self.block_id,
                            "context": self.context.absolute_url(),
                        },
                    ),
                    context=self.request,
                ),
            )
        if not self.form_data:
            raise BadRequest(
                translate(
                    _(
                        "empty_form_data",
                        default="Empty form data.",
                    ),
                    context=self.request,
                )
            )

        self.validate_schema()
        self.validate_attachments()
        if self.block.get("captcha", False):
            body = self.body if self.body else {}
            getMultiAdapter(
                (self.context, self.request),
                ICaptchaSupport,
                name=self.block["captcha"],
            ).verify(body)

    def validate_schema(self):
        schema = fix_block_schema(self.block).get("schema", {})
        validator = jsonschema.Draft202012Validator(schema)
        errors = []
        raw_errors = list(validator.iter_errors(self.form_data))
        for err in raw_errors:
            error = {"message": err.message}
            if err.path:
                error["field"] = ".".join(err.path)
            errors.append(error)
        if errors:
            raise BadRequest(json.dumps(errors))

    def validate_attachments(self):
        attachments_limit = os.environ.get("FORM_ATTACHMENTS_LIMIT", "")
        if not attachments_limit:
            return
        attachments = self.submission_context.get_attachments()
        attachments_len = 0
        for attachment in attachments.values():
            data = attachment.get("data", "")
            attachments_len += (len(data) * 3) / 4 - data.count("=", -2)
        if attachments_len > float(attachments_limit) * pow(1024, 2):
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(attachments_len, 1024)))  # noqa: RUF046
            p = math.pow(1024, i)
            s = round(attachments_len / p, 2)
            uploaded_str = f"{s} {size_name[i]}"
            raise BadRequest(
                translate(
                    _(
                        "attachments_too_big",
                        default="Attachments too big. You uploaded ${uploaded_str},"
                        " but limit is ${max} MB. Try to compress files.",
                        mapping={
                            "max": attachments_limit,
                            "uploaded_str": uploaded_str,
                        },
                    ),
                    context=self.request,
                )
            )

    def get_block_data(self, block_id):
        blocks = get_blocks(self.context)
        if not blocks:
            return {}
        for id_, block in blocks.items():
            if id_ != block_id:
                continue
            block_type = block.get("@type", "")
            if block_type != "schemaForm":
                continue
            return block
        return {}

    def _process_post(self) -> None:
        body = json_body(self.request)
        self.body = body
        self.block_id = ""
        self.block = {}
        schema = {}

        if block_id := body.get("block_id", ""):
            self.block_id = block_id
            self.block = self.get_block_data(block_id=block_id)
            schema = self.block.get("schema", {})

        self.form_data = self.cleanup_data(schema, body.get("data", {}))
        self.submission_context = FormSubmissionContext(
            context=self.context,
            request=self.request,
            block=self.block,
            form_data=self.form_data,
        )

    def reply(self) -> dict:
        # Process form submission
        self._process_post()

        # Validate form data and required parameters
        self.validate_form()

        # Disable CSRF protection
        alsoProvides(self.request, IDisableCSRFProtection)
        notify(PostEvent(self.submission_context))

        # Run form submission handlers
        self._run_handlers(self.submission_context)

        data_without_attachments = {
            k: v for k, v in self.form_data.items() if type(v) is not dict
        }
        return {"data": data_without_attachments}
