from collections import deque
from plone.keyring.interfaces import IKeyManager
from zope.component import getUtility

import base64
import copy
import json
import pyotp


EMAIL_OTP_LIFETIME = 5 * 60


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


def generate_email_token(uid="", email=""):
    """Generates the email verification token"""
    keymanager = getUtility(IKeyManager)
    token = str(base64.b32encode((uid + email + keymanager.secret()).encode()))
    totp = pyotp.TOTP(token)

    return totp.now()


def validate_email_token(uid="", email="", token=""):
    keymanager = getUtility(IKeyManager)
    expected_token = str(base64.b32encode((uid + email + keymanager.secret()).encode()))
    totp = pyotp.TOTP(expected_token)

    return totp.verify(token, valid_window=EMAIL_OTP_LIFETIME)
