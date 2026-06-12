from .interfaces import FormSubmissionContext
from .interfaces import IPostEvent
from zope.interface import implementer


@implementer(IPostEvent)
class PostEvent:
    """An event triggered when a form is submitted."""

    def __init__(self, context: FormSubmissionContext):
        self.context = context
