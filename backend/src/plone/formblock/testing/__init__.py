from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import quickInstallProduct
from plone.testing.zope import WSGI_SERVER_FIXTURE


class Layer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.formblock
        import plone.formblock.testing

        self.loadZCML(package=plone.formblock)
        self.loadZCML(package=plone.formblock.testing)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.restapi:blocks")
        applyProfile(portal, "plone.formblock:default")
        quickInstallProduct(portal, "collective.MockMailHost")
        applyProfile(portal, "collective.MockMailHost:default")

        # Set the email from address and name to avoid validation errors
        # when sending emails
        api.portal.set_registry_record(
            "plone.email_from_address", "site_addr@plone.com"
        )
        api.portal.set_registry_record("plone.email_from_name", "Plone test site")

        # Mock the validate email token function
        def validate_email_token_mock(*args, **kwargs):
            return True

        from plone.formblock import utils

        utils.validate_email_token = validate_email_token_mock


FIXTURE = Layer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="Layer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="Layer:FunctionalTesting",
)
