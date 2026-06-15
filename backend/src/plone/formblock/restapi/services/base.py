from plone.dexterity.content import DexterityContent
from plone.restapi.services import Service
from zope.publisher.http import HTTPRequest


class BaseService(Service):
    context: DexterityContent
    request: HTTPRequest

    def __init__(self, context, request):
        self.context = context
        self.request = request
