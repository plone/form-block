from plone.dexterity.content import DexterityContent
from plone.dexterity.interfaces import IDexterityContent
from plone.formblock import logger
from plone.formblock import types as t
from plone.formblock.interfaces import IFormDataStore
from plone.formblock.utils import datamanager as dm
from plone.formblock.utils import get_blocks
from plone.restapi.deserializer import json_body
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from souper.interfaces import ICatalogFactory
from souper.soup import get_soup
from souper.soup import NodeAttributeIndexer
from souper.soup import Record
from souper.soup import Soup
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.http import HTTPRequest


@implementer(ICatalogFactory)
class FormDataSoupCatalogFactory:
    def __call__(self, context: DexterityContent):
        # do not set any index here..maybe on each form
        catalog = Catalog()
        block_id_indexer = NodeAttributeIndexer("block_id")
        catalog["block_id"] = CatalogFieldIndex(block_id_indexer)
        return catalog


@implementer(IFormDataStore)
@adapter(IDexterityContent, Interface)
class FormDataStore:
    context: DexterityContent
    request: HTTPRequest
    _block_id: str = ""

    def __init__(self, context: DexterityContent, request: HTTPRequest):
        self.context = context
        self.request = request

    @property
    def soup(self) -> Soup:
        """Return the soup for form data, creating it if it doesn't exist."""
        return get_soup("form_data", self.context)

    @property
    def block_id(self) -> str:
        """Get block_id from request data."""
        if not self._block_id:
            data = json_body(self.request)
            if not data:
                data = self.request.form
            self._block_id = data.get("block_id", "")
        return self._block_id

    def get_form_fields(self) -> list[t.FieldInfo]:
        """Get the form fields for the current block."""
        blocks = get_blocks(self.context)
        if not blocks:
            return []
        block = blocks.get(self.block_id, {})
        return dm.get_schema_fields_from_block(block)

    def add(self, data: list[t.FieldData]) -> int | None:
        """Add a new record to the soup with the provided data."""
        form_fields = self.get_form_fields()
        if not form_fields:
            logger.error(
                f'Block with id {self.block_id} and type "schemaForm" not found in context: {self.context.absolute_url()}.'  # noqa: E501
            )
            return None
        record = dm.record_from_form_data(data, self.block_id, form_fields)
        soup = self.soup
        return soup.add(record)

    def length(self) -> int:
        """Return the number of records in the soup."""
        data = self.soup.data.values()
        return len(list(data))

    def search(self, query=None) -> list[Record]:
        """Search for records in the soup matching the query."""
        if not query:
            records = sorted(
                self.soup.data.values(),
                key=lambda k: k.attrs.get("date", ""),
                reverse=True,
            )
        return records

    def delete(self, id_: int) -> None:
        """Delete a record from the soup by its id."""
        record = self.soup.get(id_)
        del self.soup[record]

    def clear(self) -> None:
        """Clear all records from the soup."""
        self.soup.clear()
