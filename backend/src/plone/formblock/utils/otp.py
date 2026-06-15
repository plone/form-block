from plone.keyring.interfaces import IKeyManager
from zope.component import getUtility

import base64
import pyotp


EMAIL_OTP_LIFETIME = 5 * 60


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
