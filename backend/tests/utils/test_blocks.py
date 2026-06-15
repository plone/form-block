"""Unit tests for plone.formblock.utils.blocks.

Covers the block-traversal and schema-normalization helpers:
``flatten_block_hierachy``, ``get_blocks`` and ``fix_block_schema``. These are
pure functions, so they run as plain unit tests with fixtures and
parametrization (``get_blocks`` only needs an object exposing a ``blocks``
attribute, faked with ``SimpleNamespace``).
"""

from plone.formblock.utils.blocks import fix_block_schema
from plone.formblock.utils.blocks import flatten_block_hierachy
from plone.formblock.utils.blocks import get_blocks
from types import SimpleNamespace

import json
import pytest


@pytest.fixture
def nested_blocks() -> dict:
    """Top-level blocks plus one nested via ``data.blocks`` and one via ``blocks``."""
    return {
        "a": {"@type": "text"},
        "b": {
            "@type": "columns",
            "data": {"blocks": {"c": {"@type": "schemaForm"}}},
        },
        "d": {"@type": "group", "blocks": {"e": {"@type": "text"}}},
    }


@pytest.fixture
def make_context():
    """Factory returning a fake context object with a ``blocks`` attribute."""

    def factory(blocks):
        return SimpleNamespace(blocks=blocks)

    return factory


class TestFlattenBlockHierarchy:
    def test_empty(self):
        assert list(flatten_block_hierachy({})) == []

    def test_flat_blocks(self):
        blocks = {"a": {"@type": "text"}, "b": {"@type": "image"}}
        assert set(dict(flatten_block_hierachy(blocks))) == {"a", "b"}

    def test_includes_all_nested(self, nested_blocks):
        assert set(dict(flatten_block_hierachy(nested_blocks))) == {
            "a",
            "b",
            "c",
            "d",
            "e",
        }

    def test_count_includes_nested(self, nested_blocks):
        assert len(list(flatten_block_hierachy(nested_blocks))) == 5

    def test_data_blocks_nesting(self):
        blocks = {
            "col": {
                "@type": "columns",
                "data": {"blocks": {"inner": {"@type": "text"}}},
            }
        }
        assert set(dict(flatten_block_hierachy(blocks))) == {"col", "inner"}

    def test_direct_blocks_nesting(self):
        blocks = {"g": {"@type": "group", "blocks": {"inner": {"@type": "text"}}}}
        assert set(dict(flatten_block_hierachy(blocks))) == {"g", "inner"}

    def test_deeply_nested(self):
        blocks = {
            "l1": {
                "@type": "group",
                "blocks": {
                    "l2": {"@type": "group", "blocks": {"l3": {"@type": "text"}}},
                },
            }
        }
        assert set(dict(flatten_block_hierachy(blocks))) == {"l1", "l2", "l3"}

    @pytest.mark.parametrize(
        "data",
        [{}, None, "notadict", {"foo": "bar"}, []],
        ids=["empty-dict", "none", "string", "dict-without-blocks", "list"],
    )
    def test_data_without_blocks_yields_only_self(self, data):
        blocks = {"x": {"@type": "text", "data": data}}
        assert set(dict(flatten_block_hierachy(blocks))) == {"x"}


class TestGetBlocks:
    def test_dict_blocks(self, make_context, nested_blocks):
        result = get_blocks(make_context(nested_blocks))
        assert set(result) == {"a", "b", "c", "d", "e"}

    def test_json_string_blocks(self, make_context, nested_blocks):
        result = get_blocks(make_context(json.dumps(nested_blocks)))
        assert set(result) == {"a", "b", "c", "d", "e"}

    def test_missing_blocks_attribute(self):
        assert get_blocks(SimpleNamespace()) == {}

    @pytest.mark.parametrize("blocks", [{}, "{}"], ids=["empty-dict", "empty-json"])
    def test_empty_blocks(self, make_context, blocks):
        assert get_blocks(make_context(blocks)) == {}

    def test_does_not_mutate_context(self, make_context):
        blocks = {"x": {"@type": "text", "blocks": {"y": {"@type": "text"}}}}
        context = make_context(blocks)
        result = get_blocks(context)
        result["x"]["injected"] = True
        assert "injected" not in context.blocks["x"]


class TestFixBlockSchema:
    @pytest.mark.parametrize(
        "field,value,expected",
        [
            ("minLength", "3", 3),
            ("maxLength", "10", 10),
            ("minLength", "0", 0),
        ],
    )
    def test_casts_string_length_to_int(self, field, value, expected):
        block = {"schema": {"properties": {"f": {field: value}}}}
        out = fix_block_schema(block)
        prop = out["schema"]["properties"]["f"]
        assert prop[field] == expected
        assert isinstance(prop[field], int)

    def test_leaves_int_value_unchanged(self):
        block = {"schema": {"properties": {"f": {"minLength": 5}}}}
        out = fix_block_schema(block)
        assert out["schema"]["properties"]["f"]["minLength"] == 5

    def test_leaves_other_keys_unchanged(self):
        block = {"schema": {"properties": {"f": {"title": "Name", "minLength": "2"}}}}
        out = fix_block_schema(block)
        prop = out["schema"]["properties"]["f"]
        assert prop["title"] == "Name"
        assert prop["minLength"] == 2

    def test_multiple_properties(self):
        block = {
            "schema": {
                "properties": {
                    "a": {"minLength": "1", "maxLength": "5"},
                    "b": {"maxLength": "9"},
                }
            }
        }
        out = fix_block_schema(block)
        props = out["schema"]["properties"]
        assert props["a"]["minLength"] == 1
        assert props["a"]["maxLength"] == 5
        assert props["b"]["maxLength"] == 9

    @pytest.mark.parametrize(
        "block",
        [
            {"@type": "x"},
            {"schema": {}},
            {"schema": {"properties": {}}},
        ],
        ids=["no-schema", "empty-schema", "no-properties"],
    )
    def test_no_properties_returns_block(self, block):
        assert fix_block_schema(block) == block

    def test_returns_same_object(self):
        block = {"schema": {"properties": {"f": {"minLength": "1"}}}}
        assert fix_block_schema(block) is block
