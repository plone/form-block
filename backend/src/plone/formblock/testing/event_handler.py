from plone.formblock.events import PostEvent
from plone.formblock.interfaces import FormSubmissionContext

import os


def event_handler(event: PostEvent):
    """Dummy event handler for testing purposes.

    If the environment variable __TEST_EVENT_HANDLER is set,
    It adds a field to the form data
    """
    if os.environ.get("__TEST_EVENT_HANDLER"):
        context: FormSubmissionContext = event.context
        context.form_data["reply"] = "hello"
