# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0a3 (2026-07-07)


### New features:

- Added forwarding of request HTTP headers configured on the form block (``httpHeaders``, one header name per line) into the administration email. @ericof [#21](https://github.com/plone/form-block/issues/21)


### Bug fixes:

- Fixed the form email processor ignoring the block's configured settings: the selected mail template, admin info, mail header/footer and sender/recipient addresses are now honored when a form is submitted. @ericof [#19](https://github.com/plone/form-block/issues/19)


### Internal:

- Moved the mail templates setting to a ``JSONField`` (``schemaform.mail_templates_json``), deprecating ``schemaform.mail_templates``, with an upgrade step that migrates existing templates. @ericof [#19](https://github.com/plone/form-block/issues/19)


### Tests

- Added a dedicated GenericSetup testing profile to configure mail and captcha settings for the test suite. @ericof 

## 1.0.0a2 (2026-06-18)


### Bug fixes:

- Cast `minLength` / `maxLength` to integers before validating submissions, so string-valued length constraints no longer break form validation. @ericof 


### Internal:

- Rename internal package to plone.formblock @ericof [#7](https://github.com/plone/form-block/issues/7)
- Rewrite all backend tests @ericof [#8](https://github.com/plone/form-block/issues/8)
- Added `Products.PrintingMailHost` to the development environment to print outgoing emails to the log. @ericof [#11](https://github.com/plone/form-block/issues/11)
- Added example content with pages using form blocks, plus default captcha and mail configuration, to the `initial` profile. @ericof [#12](https://github.com/plone/form-block/issues/12)
- Refactored `EmailFormProcessor`, extracting reusable e-mail helpers (`create_message`, `is_mailhost_configured`, `substitute_variables`) and splitting the admin and confirmation message building. @ericof [#13](https://github.com/plone/form-block/issues/13)
- Refactored the captcha providers onto a shared `ExternalCaptchaSupport` base class, added reCAPTCHA v3 support (via `recaptcha.net` and a configurable score threshold), and standardized the serialized `provider` key across providers. @ericof [#14](https://github.com/plone/form-block/issues/14)
- Refactored the form data store: extracted the schema-field and record builders into `utils/datamanager.py` with type hints and `TypedDict` definitions, and added a `total_records_in_block` helper. @ericof [#16](https://github.com/plone/form-block/issues/16)
- Moved the captcha-provider and mail-template vocabularies into a dedicated `vocabularies` package, with tests. @ericof 
- Removed the redundant legacy `FormSerializer` block serializer, now fully superseded by `SchemaFormBlockSerializer`. @ericof 
- Updated the i18n message catalogs. @ericof 


### Documentation:

- Update README.md file. @ericof
