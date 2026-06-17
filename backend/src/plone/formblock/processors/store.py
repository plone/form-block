from plone.formblock.interfaces import FormSubmissionContext
from plone.formblock.interfaces import IFormDataStore
from plone.formblock.interfaces import IFormSubmissionProcessor
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(IFormSubmissionProcessor)
@adapter(FormSubmissionContext)
class StoreFormProcessor:
    """Stores submitted form data"""

    order = 2

    def __init__(self, context: FormSubmissionContext):
        self.context = context.context
        self.request = context.request
        self.block = context.block
        self.form_data = context.form_data
        self.records = context.get_records()

    def __call__(self) -> None:
        if not self.block.get("store"):
            return

        store = getMultiAdapter((self.context, self.request), IFormDataStore)
        res = store.add(data=self.records)
        if not res:
            raise BadRequest("Unable to store data")
