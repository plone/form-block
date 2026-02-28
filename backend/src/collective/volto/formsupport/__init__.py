"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


__version__ = "1.0.0a0"

PACKAGE_NAME = "collective.volto.formsupport"

logger = logging.getLogger(PACKAGE_NAME)
_ = MessageFactory(PACKAGE_NAME)
