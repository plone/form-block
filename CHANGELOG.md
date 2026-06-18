# Change log

<!-- You should *NOT* be adding new change log entries to this file.
     You should create a file in the news directory instead.
     For helpful instructions, please see:
     https://6.docs.plone.org/contributing/index.html#contributing-change-log-label
-->

<!-- towncrier release notes start -->
## 1.0.0a2 (2026-06-18)

### Backend


#### Bug fixes:

- Cast `minLength` / `maxLength` to integers before validating submissions, so string-valued length constraints no longer break form validation. @ericof 


#### Internal:

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


#### Documentation:

- Update README.md file. @ericof 



### Frontend

#### Feature

- Added a data view to the form block editor to see the number of stored submissions, export them to CSV, and clear them. @ericof [#16](https://github.com/plone/form-block/issues/16)

#### Bugfix

- Fix Honeypot widget. @ericof 
- Fix NoRobots widget. @ericof 
- Fix the Google reCAPTCHA v3 widget to mint a fresh token on submit (instead of pinning the initial, undefined one) and load the script from `recaptcha.net`. @ericof 

#### Internal

- Rewrote the `volto-form-block` frontend in TypeScript (widgets, wrappers, blocks, actions, reducers, helpers and configuration). @ericof [#10](https://github.com/plone/form-block/issues/10)
- Replaced `moment` with the native `Intl.DateTimeFormat` API for date and time formatting in the form view. @ericof 
- Update Volto to 19.1.4. @ericof 
- Updated the i18n message catalogs. @ericof 

#### Documentation

- Added Storybook stories for the DataTable, ThankYou, and captcha widget components. @ericof 
- Update README.md file. @ericof 



### Project


#### Internal

- Reorganize repository according to the latest changes in cookieplone-templates. @ericof [#6](https://github.com/plone/form-block/pull/6)
- Update storybook deployment. @ericof 


#### Documentation

- Update README.md file. @ericof 




## 1.0.0-alpha.1 (2026-03-04)

### Frontend
#### Internal

- Pending backports from the feature branches. @robgietema

## 1.0.0-alpha.0 (2025-11-14)

### Frontend
#### Internal

- Move to the new setup @sneridagh [#109](https://github.com/plone/form-block/issue/109)
