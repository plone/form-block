from collections import deque

import copy
import json


def flatten_block_hierachy(blocks):
    """Given some blocks, return all contained blocks, including "subblocks"
    This allows embedding the form block into something like columns datastorage
    """

    queue = deque(list(blocks.items()))

    while queue:
        blocktuple = queue.pop()
        yield blocktuple

        block_value = blocktuple[1]
        block_value_data = block_value.get("data", {})
        if (
            block_value_data
            and isinstance(block_value_data, dict)
            and "blocks" in block_value_data
        ):
            queue.extend(list(block_value_data["blocks"].items()))

        if "blocks" in block_value:
            queue.extend(list(block_value["blocks"].items()))


def get_blocks(context):
    """Returns all blocks from a context, including those coming from slots"""

    blocks = copy.deepcopy(getattr(context, "blocks", {}))
    if isinstance(blocks, str):
        blocks = json.loads(blocks)

    flat = list(flatten_block_hierachy(blocks)) if blocks else []

    return dict(flat)


def fix_block_schema(block: dict) -> dict:
    schema = block.get("schema", {})
    properties = schema.get("properties", {})
    to_cast = {
        "minLength": int,
        "maxLength": int,
    }
    for prop_name, prop in properties.items():
        for key, value in prop.items():
            if key in to_cast and isinstance(value, str):
                properties[prop_name][key] = to_cast[key](value)
    return block
