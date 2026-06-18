# Form Block (@plone/volto-form-block)

A Plone add-on supporting the creation of forms inside blocks.

[![npm](https://img.shields.io/npm/v/@plone/volto-form-block)](https://www.npmjs.com/package/@plone/volto-form-block)
[![](https://img.shields.io/badge/-Storybook-ff4785?logo=Storybook&logoColor=white&style=flat-square)](https://plone.github.io/form-block/)
[![CI](https://github.com/plone/form-block/actions/workflows/main.yml/badge.svg)](https://github.com/plone/form-block/actions/workflows/main.yml)

## Features

This add-on adds the Form block and the needed reducers to your project.

### Block selection

![Blocks Chooser](https://raw.githubusercontent.com/plone/form-block/refs/heads/main/docs/form-block-chooser.png)

### Creation / Edit

![Editing a block](https://raw.githubusercontent.com/plone/form-block/refs/heads/main/docs/form-creation.png)

### Form view

![Form view](https://raw.githubusercontent.com/plone/form-block/refs/heads/main/docs/form-block-view.png)

### Confirmation page

![Confirmation page](https://raw.githubusercontent.com/plone/form-block/refs/heads/main/docs/form-block-confirmation.png)

### View stored data / export data

![Data view](https://raw.githubusercontent.com/plone/form-block/refs/heads/main/docs/form-block-data-view.png)

## Installation

This add-on requires **Volto 19 or later**.

Add `@plone/volto-form-block` to your `package.json`.

```json
"addons": [
    ...
    "@plone/volto-form-block"
],
"dependencies": {
    "@plone/volto-form-block": "*"
}
```

## Test installation

Visit http://localhost:3000/ in a browser, log in, and add a **Form** block to a page.


## Customizing the Form Block

This guide explains how to customize and extend the `volto-form-block` package, using the example project as a reference.

> Note: references to `@plone/volto-form-block` imports, email addresses, and sender names in the examples are specific to that project — replace them with your own values.

### Overview

There are two extension points:

1. **`config.blocks.blocksConfig.schemaForm`** — block-level configuration (widgets, components, factory lists, email defaults, etc.)
2. **`config.registerUtility()`** — registering custom field types with default data and editable properties


### Registering Custom Field Types

Each custom field type needs two utility registrations:

#### `fieldFactoryInitialData`

Defines the default data when a field is added to the form schema.

```ts
config.registerUtility({
  name: 'country',
  type: 'fieldFactoryInitialData',
  method: (intl) => ({
    type: 'string',
    factory: 'country',
    choices: countries[intl.locale].map((c) => [c, c]),
    id: 'country',
  }),
});
```

| Key                 | Purpose                                                                                                                                                                    |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`              | Field data type: `string`, `boolean`, `number`, `integer`, `array`, `object`, `dict`                                                                                       |
| `widget`            | (Optional) Widget to use: `radio_group`, `checkbox_group`, `textarea`, `email`, `date`, `datetime`, `time`, `hidden`, `static_text`, `url`, `password`, `richtext`, `json` |
| `choices`           | For choice/select fields: `[[value, label], ...]`                                                                                                                          |
| `required`          | Boolean                                                                                                                                                                    |
| `title` / `default` | Label and default value                                                                                                                                                    |
| `id`                | Unique field identifier                                                                                                                                                    |

#### `fieldFactoryProperties`

Defines extra schema properties shown in the "Edit Field" sidebar. Return an empty object `{}` to show no extra fields beyond the defaults.

```ts
config.registerUtility({
  name: 'country',
  type: 'fieldFactoryProperties',
  method: (intl) => ({}),
});
```

The method receives `intl` (react-intl object) and returns a schema-like object. Keys become additional fields in the edit modal (e.g., `minLength`, `maxLength`, `default`, `choices`, `values`, `size`, `accept`, `minimum`, `maximum`).

#### Make the field selectable

Add entries to these config arrays so the field appears in the editor's "Add field" dropdown:

```ts
config.blocks.blocksConfig.schemaForm = {
  ...config.blocks.blocksConfig.schemaForm,

  additionalFactory: [
    ...config.blocks.blocksConfig.schemaForm.additionalFactory,
    { value: 'country', label: 'Country' },
  ],

  filterFactory: [
    ...config.blocks.blocksConfig.schemaForm.filterFactory,
    'country',
  ],
};
```

- **`additionalFactory`** — extra field types to append to the backend vocabulary
- **`filterFactory`** — whitelist of allowed factory names (items not in this list are hidden)

#### Exclude fields from submission

Fields listed in `filterFactorySend` are excluded from the submitted payload. This is useful for informational fields like data privacy notices:

```ts
filterFactorySend: [
  ...config.blocks.blocksConfig.schemaForm.filterFactorySend,
  'dataprotectionInfo',
],
```

---

### Block Configuration

All settings go into `config.blocks.blocksConfig.schemaForm`:

```ts
config.blocks.blocksConfig.schemaForm = {
  ...config.blocks.blocksConfig.schemaForm,
  // ...overrides
};
```

#### Email defaults

```ts
defaultSender: 'noreply@example.org',
defaultSenderName: 'Your Organization',
```

#### Form-level component

The top-level form wrapper. Receives `children`, `onSubmit`, and `error`.

```ts
component: FormComponent,
```

#### Button component

Renders submit and cancel buttons. Receives `primary`, `secondary`, `type`, `title`, `onClick`.

```ts
buttonComponent: ButtonWrapper,
```

#### Schema enhancer

A function that modifies the block's edit schema before it's rendered. Useful to replace fieldsets or add custom options.

```ts
import { formBlockSchemaEnhancer } from '../components/Blocks/Form/schema';
schemaEnhancer: formBlockSchemaEnhancer,
```

#### View/edit wrappers

Wrap the view and edit components to inject custom context (e.g., temporary component registrations):

```ts
view: viewWrapper(config.blocks.blocksConfig.schemaForm.view),
edit: viewWrapper(config.blocks.blocksConfig.schemaForm.edit),
```

### Widgets

The form block uses a **two-layer widget system**:

#### Outer layer (`widgets`)

Controls which _wrapper_ component renders for a given field type or widget. These wrappers handle edit/delete controls, layout, and delegate to an inner component.

```ts
widgets: {
  // Match by widget name
  widget: {
    textarea: TextareaWrapper,
    file: FileWrapper,
    date: DatetimeWrapper,
    time: TimeWrapper,
    datetime: DatetimeWrapper,
    email: EmailWrapper,
    radio_group: RadioGroupWrapper,
    checkbox_group: CheckboxGroupWrapper,
    hidden: HiddenWrapper,
  },
  // Match by choices presence
  choices: SelectWrapper,
  // Match by data type
  type: {
    object: FileWrapper,
    date: DatetimeWrapper,
    datetime: DatetimeWrapper,
    number: NumberWrapper,
    integer: NumberWrapper,
    boolean: CheckboxWrapper,
  },
  // Fallback
  default: TextWrapper,
}
```

Resolution order: `widget` → `choices` → `type` → `default`.

#### Inner layer (`innerWidgets`)

The actual UI components that render form inputs. These are imported from your project and referenced by the wrappers:

```ts
innerWidgets: {
  text: TextField,
  textarea: TextAreaField,
  file: FileSelector,
  date: DatePicker,
  datetime: DatePicker,
  time: TimeField,
  email: TextField,
  radioGroup: RadioGroup,
  radioGroupOption: Radio,
  number: TextField,
  checkbox: CheckboxField,
  checkboxGroup: CheckboxGroup,
  checkboxGroupOption: Checkbox,
  select: Select,
  hidden: TextField,
},
```

---

### Complete Example: Adding a Custom Field

Here's the recipe for adding a custom "Phone number" field:

1. **Register default data** — `registerUtility({ name: 'phonenumber', type: 'fieldFactoryInitialData', ... })`
2. **Register properties** — `registerUtility({ name: 'phonenumber', type: 'fieldFactoryProperties', ... })` (empty if no extra edit fields needed)
3. **Add to factory lists** — `additionalFactory`, `filterFactory`
4. **(Optional)** Add to `filterFactorySend` if it should not be submitted

Example from `schemaFormBlock.tsx`:

```ts
config.registerUtility({
  name: 'phonenumber',
  type: 'fieldFactoryProperties',
  method: (intl) => ({}),
});

config.registerUtility({
  name: 'phonenumber',
  type: 'fieldFactoryInitialData',
  method: (intl) => ({
    type: 'string',
    factory: 'phonenumber',
    id: 'phonenumber',
  }),
});

// Then in the schemaForm config:
additionalFactory: [
  ...config.blocks.blocksConfig.schemaForm.additionalFactory,
  { value: 'phonenumber', label: 'Phone number' },
],
filterFactory: [
  ...config.blocks.blocksConfig.schemaForm.filterFactory,
  'phonenumber',
],
```


## Development

The development of this add-on is done in isolation using pnpm workspaces, the latest `mrs-developer`, and other Volto core improvements.
For these reasons, it only works with pnpm and Volto 18.


### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [nvm](https://6.docs.plone.org/install/create-project-cookieplone.html#nvm)
-   [Node.js and pnpm](https://6.docs.plone.org/install/create-project.html#node-js) 24
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:plone/form-block.git
    cd form-block/frontend
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Make convenience commands

Run `make help` to list the available Make commands.


### Set up development environment

Install package requirements.

```shell
make install
```

### Start developing

Start the backend.

```shell
make backend-docker-start
```

In a separate terminal session, start the frontend.

```shell
make start
```

### Lint code

Run ESlint, Prettier, and Stylelint in analyze mode.

```shell
make lint
```

### Format code

Run ESlint, Prettier, and Stylelint in fix mode.

```shell
make format
```

### i18n

Extract the i18n messages to locales.

```shell
make i18n
```

### Unit tests

Run unit tests.

```shell
make test
```

### Run Cypress tests

Run each of these steps in separate terminal sessions.

In the first session, start the frontend in development mode.

```shell
make acceptance-frontend-dev-start
```

In the second session, start the backend acceptance server.

```shell
make acceptance-backend-start
```

In the third session, start the Cypress interactive test runner.

```shell
make acceptance-test
```

## License

The project is licensed under the MIT license.

## Credits and acknowledgements 🙏

This add-on is built on top of the awesome [volto-form-block](https://github.com/collective/volto-form-block) developed by **RedTurtle Technology**.

The current version of the codebase was developed by **kitconcept GmbH** and sponsored by the **Fachhochschule Nordwestschweiz**.

Generated using [Cookieplone (2.0.0b3)](https://github.com/plone/cookieplone) and [cookieplone-templates (6678734)](https://github.com/plone/cookieplone-templates/commit/6678734cc3713f3fab9ea510616cef59dc466514) on 2026-06-10 18:43:35.112495. A special thanks to all contributors and supporters!
