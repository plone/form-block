# plone.formblock

A Plone add-on supporting the creation of forms inside blocks.

## Features

### Send submissions by email

When the **Send** action is enabled on a form block, each submission is emailed to the configured recipients. The subject, sender and recipients are configured on the block, and the submitted values are rendered into the message body.

### Store submissions

When the **Store data** action is enabled, each submission is stored on the content object. Stored submissions can be reviewed, exported to CSV and cleared directly from the form block editor in Volto.

### Captcha support

Captcha support requires a specific name adapter that implements ICaptchaSupport. This product contains implementations for:

* HCaptcha (plone.formwidget.hcaptcha)
* Google ReCaptcha (plone.formwidget.recaptcha)
* Custom questions and answers (collective.z3cform.norobots)
* Honeypot (collective.honeypot)

Each implementation must be included, installed and configured separately.

To include one implementation, you need to install the egg with the needed extras_require:

* plone.formblock[recaptcha]
* plone.formblock[hcaptcha]
* plone.formblock[norobots]
* plone.formblock[honeypot]

During the form post, the token captcha will be verified with the defined captcha method.

#### Honeypot configuration

If honeypot dependency is available in your installation, the honeypot validation is enabled and selectable in forms.

Default field name is **protected_1** and you can change it with an environment variable. See the [collective.honeypot configuration](https://github.com/collective/collective.honeypot?tab=readme-ov-file#configuration) for details.

### Attachments upload limits

Forms can have one or more attachment field to allow users to upload some files.

These files will be sent via mail, so it could be a good idea setting a limit to them. For example if you use GMail as mail server, you can't send messages with attachments > 25MB.

There is an environment variable that you can use to set that limit (in MB):

```bash
export FORM_ATTACHMENTS_LIMIT=25
```

By default this is not set.

The upload limit is also passed to the frontend in the form data with the attachments_limit key.

### Content-transfer-encoding

It is possible to set the content-transfer-encoding for the email body, settings the environment variable `MAIL_CONTENT_TRANSFER_ENCODING`:

```bash
export MAIL_CONTENT_TRANSFER_ENCODING=base64
```

This is useful for some SMTP servers that have problems with quoted-printable encoding.

By default the content-transfer-encoding is quoted-printable as overridden in [Products.MailHost](https://github.com/zopefoundation/Products.MailHost/blob/master/src/Products/MailHost/MailHost.py#L65)

### Email subject templating

You can also interpolate the form values to the email subject using the field id, in this way: `${field_name}`

### Header forwarding

It is possible to configure some headers from the form POST request to be included in the email's headers by configuring the httpHeaders field in your Volto block.

The [@plone/volto-form-block](https://www.npmjs.com/package/@plone/volto-form-block) package allows the following headers to be forwarded:

* `HTTP_X_FORWARDED_FOR`
* `HTTP_X_FORWARDED_PORT`
* `REMOTE_ADDR`
* `PATH_INFO`
* `HTTP_USER_AGENT`
* `HTTP_REFERER`

## Installation

Install plone.formblock with uv:

```shell
uv add plone.formblock
```

Or with pip:

```shell
pip install plone.formblock
```

Create the Plone site.

```shell
make create-site
```

## Contribute

- [Issue tracker](https://github.com/plone/form-block/issues)
- [Source code](https://github.com/plone/form-block/)

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository.

    ```shell
    git clone git@github.com:plone/form-block.git
    cd form-block/backend
    ```

2.  Install this code base.

    ```shell
    make install
    ```


## License

The project is licensed under GPLv2.

## Credits and acknowledgements 🙏

This add-on is built on top of the awesome [collective.volto.formsupport](https://github.com/collective/collective.volto.formsupport) developed by **RedTurtle Technology**.

The current version of the codebase was developed by **kitconcept GmbH** and sponsored by the **Fachhochschule Nordwestschweiz**.

Generated using [Cookieplone (2.0.0b3)](https://github.com/plone/cookieplone) and [cookieplone-templates (6678734)](https://github.com/plone/cookieplone-templates/commit/6678734cc3713f3fab9ea510616cef59dc466514) on 2026-06-10 18:43:35.112495. A special thanks to all contributors and supporters!
