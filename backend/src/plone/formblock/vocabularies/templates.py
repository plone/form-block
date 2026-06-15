from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def mail_templates_vocabulary_factory(context):
    name = "schemaform.mail_templates"
    registry_record_value = api.portal.get_registry_record(name)
    items = list(registry_record_value.keys())
    return SimpleVocabulary.fromItems([[item, item, item] for item in items])
