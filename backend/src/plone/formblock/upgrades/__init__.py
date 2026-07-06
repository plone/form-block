from plone import api
from plone.formblock import logger
from plone.formblock.interfaces import DEFAULT_TEMPLATE
from Products.GenericSetup.tool import SetupTool


def migrate_mail_templates(context: SetupTool) -> None:
    """Migrate mail templates from the old registry record to the new one."""
    default_templates = {"default": DEFAULT_TEMPLATE}
    old_templates: dict[str, str] = api.portal.get_registry_record(
        "schemaform.mail_templates", default=default_templates
    )
    api.portal.set_registry_record("schemaform.mail_templates_json", old_templates)
    # Set the old registry record to an empty dict to avoid confusion
    api.portal.set_registry_record("schemaform.mail_templates", {})
    logger.info(
        "Migrated mail templates from 'schemaform.mail_templates' to "
        "'schemaform.mail_templates_json'."
    )
