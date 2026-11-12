---
block: schemaForm
---

Shows a form that visitors fill in. When the form is submitted, the answers can be stored in the site, emailed to the administrators, emailed back to the visitor, or any combination of these. The block stores its own settings and the `schema` that describes its fields. The answers are not stored in the block: they are sent to the `@schemaform-data` endpoint of the content item that holds the block.

### Settings

- `title`, `description`: optional heading and text shown above the form.
- `submit_label`: text of the submit button.
- `show_cancel`: `true` to show a cancel button. Its text is `cancel_label`.
- `success`: text shown before the submitted answers when the visitor is not redirected.
- `thankyou`: text of the thank you message. `${formfields}` lists all answers, and `${field_id}` shows one answer.
- `forward_user_to`: optional list with one item, `[{ "@id": "/path-or-url" }]`. When it is set, the visitor is redirected there after submitting, and the thank you message is not shown.
- `captcha`: id of the captcha provider, such as `honeypot`. `captcha_props` is an object with the settings of the provider, such as `{ "provider": "..." }`. The submission is only checked against the provider when `captcha` is set.
- `store`: `true` to keep the answers in the site. `data_wipe`: number of days after which the stored answers are deleted. Use `-1` to keep them indefinitely.
- `send`: `true` to email the answers to the administrators. The addresses are in `recipients`, a semicolon-separated list. `bcc` is an optional list of blind copy addresses. `admin_info` and `httpHeaders` add text to that email. `httpHeaders` is a list of request header names, one per line, whose values are added to the email.
- `send_confirmation`: `true` to email a confirmation to the visitor. `confirmation_recipients` is the field of the form that holds the visitor's address, written as `${field_id}`. `fixed_attachment` is a file attached to every confirmation, and `mail_template` is the name of the mail template to use.
- `sender`, `sender_name`, `subject`: the sender of the emails and the subject of the email. They are used when `send` or `send_confirmation` is `true`.
- `mail_header`, `mail_footer`: rich text at the beginning and at the end of the email, stored as an object with the HTML in `data`, such as `{ "data": "<p>Hello</p>" }`.

Values of `sender`, `sender_name`, `bcc` and `confirmation_recipients` can contain `${field_id}`, which is replaced with the answer to that field.

### Fields

`schema` is a JSON schema with the fields of the form:

- `fieldsets`: a list of `{ "id", "title", "fields" }` objects. `fields` lists the field ids in the order they are shown. The submitted answers are kept in this order.
- `properties`: an object keyed by field id. Each field has an `id`, a `title`, and a `type` (`string`, `boolean`, `integer`, `number`, `array` or `object`). It can also have a `description`, a `placeholder`, a `default`, and a `factory` that names the kind of field, such as `label_text_field`, `label_email`, `label_choice_field`, `label_boolean_field`, `label_date_field`, `label_datetime_field`, `textarea`, `radio_group`, `checkbox_group`, `number`, `time`, `hidden`, `static_text` or `File Upload`. Choice fields list their options in `choices`, as `[value, label]` pairs. `minLength` and `maxLength` can be given as strings: the backend converts them to numbers.
- `required`: a list of the field ids that must be filled in.

### Submit

The visitor's browser sends a `POST` to `<content>/@schemaform-data` with the body `{ "block_id", "data" }`, and `captcha` when the form uses one. The backend finds the block by `block_id` in the content item, and keeps only the answers whose field id is in `schema.properties`. It then checks the answers against `schema` with JSON Schema (Draft 2020-12), so `required`, types and lengths are enforced. Invalid answers are rejected with a `400` response that lists each error and its field. The response contains the answers, without file attachments.

### Example

A contact form with three fields. Its answers are stored in the site and nothing is emailed.

```json
{
  "@type": "schemaForm",
  "title": "Contact us",
  "description": "We want to know more about you",
  "submit_label": "Submit",
  "show_cancel": false,
  "success": "Thank you! You have submitted the following data:",
  "thankyou": "Those were your answers:\n${formfields}",
  "store": true,
  "data_wipe": -1,
  "send": false,
  "send_confirmation": false,
  "schema": {
    "fieldsets": [
      {
        "id": "default",
        "title": "Default",
        "fields": ["name", "email", "message"]
      }
    ],
    "properties": {
      "name": {
        "id": "name",
        "title": "Your name",
        "description": "Please, tell us your name",
        "placeholder": "John Smith",
        "factory": { "label": "Text", "value": "label_text_field" },
        "type": "string"
      },
      "email": {
        "id": "email",
        "title": "E-mail",
        "description": "Your e-mail",
        "factory": "label_email",
        "type": "string",
        "widget": "email"
      },
      "message": {
        "id": "message",
        "title": "Additional information",
        "factory": "textarea",
        "type": "string",
        "widget": "textarea",
        "minLength": "50"
      }
    },
    "required": ["name", "email", "message"]
  }
}
```
