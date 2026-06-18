# Form Block 🚀

A Plone add-on supporting the creation of forms inside blocks.

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/plone.formblock)](https://pypi.org/project/plone.formblock/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/plone.formblock)](https://pypi.org/project/plone.formblock/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/plone.formblock)](https://pypi.org/project/plone.formblock/)
[![PyPI - License](https://img.shields.io/pypi/l/plone.formblock)](https://pypi.org/project/plone.formblock/)
[![PyPI - Status](https://img.shields.io/pypi/status/plone.formblock)](https://pypi.org/project/plone.formblock/)

</div>

<div align="center">

[![npm](https://img.shields.io/npm/v/@plone/volto-form-block)](https://www.npmjs.com/package/@plone/volto-form-block)
[![](https://img.shields.io/badge/-Storybook-ff4785?logo=Storybook&logoColor=white&style=flat-square)](https://plone.github.io/form-block/)

</div>

<div align="center">

[![CI](https://github.com/plone/form-block/actions/workflows/main.yml/badge.svg)](https://github.com/plone/form-block/actions/workflows/main.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookieplone-0083be.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)

[![GitHub contributors](https://img.shields.io/github/contributors/plone/form-block)](https://github.com/plone/form-block)
[![GitHub Repo stars](https://img.shields.io/github/stars/plone/form-block?style=social)](https://github.com/plone/form-block)

</div>

## About Form Block

This add-on is composed of two packages:

* Backend: [`plone.formblock`](https://pypi.org/project/plone.formblock/), for Plone 6.1 and 6.2.
* Frontend: [`@plone/volto-form-block`](https://www.npmjs.com/package/@plone/volto-form-block), for Volto 19 or later.

In order to have the complete solution you need to install both of them in your project, please follow the instructions: [`backend`](./backend/README.md) and [`frontend`](./frontend/README.md).

### Relation to collective.volto.formsupport / volto-form-block

This add-on began as an evolution of RedTurtle Technology's [volto-form-block](https://github.com/collective/volto-form-block) and [collective.volto.formsupport](https://github.com/collective/collective.volto.formsupport), but has since taken its own direction and is not compatible with forms created by those add-ons.

## Quick Start 🏁

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [nvm](https://6.docs.plone.org/install/create-project-cookieplone.html#nvm)
-   [Node.js and pnpm](https://6.docs.plone.org/install/create-project.html#node-js) 24
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)


### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:plone/form-block.git
    cd form-block
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Fire Up the Servers 🔥

1.  Create a new Plone site on your first run.

    ```shell
    make backend-create-site
    ```

2.  Start the backend at http://localhost:8080/.

    ```shell
    make backend-start
    ```

3.  In a new shell session, start the frontend at http://localhost:3000/.

    ```shell
    make frontend-start
    ```

Voila! Your Plone site should be live and kicking! 🎉

### Local Stack Deployment 📦

Deploy a local Docker Compose environment that includes the following.

- Docker images for Backend and Frontend 🖼️
- A stack with a Traefik router and a PostgreSQL database 🗃️
- Accessible at [http://form-block.localhost](http://form-block.localhost) 🌐

Run the following commands in a shell session.

```shell
make stack-create-site
make stack-start
```

And... you're all set! Your Plone site is up and running locally! 🚀

## Project structure 🏗️

This monorepo consists of the following distinct sections:

- **backend**: Houses the API and Plone installation, utilizing pip instead of buildout, and includes a policy package named plone.formblock.
- **frontend**: Contains the React (Volto) package.
- **devops**: Encompasses Docker stack, Ansible playbooks, and cache settings.
- **docs**: Scaffold for writing documentation for your project.

### Why this structure? 🤔

- All necessary codebases to run the site are contained within the repository (excluding existing add-ons for Plone and React).
- Specific GitHub Workflows are triggered based on changes in each codebase (refer to .github/workflows).
- Simplifies the creation of Docker images for each codebase.
- Demonstrates Plone installation/setup without buildout.

## Code quality assurance 🧐

To check your code against quality standards, run the following shell command.

```shell
make check
```

### Format the codebase

To format and rewrite the code base, ensuring it adheres to quality standards, run the following shell command.

```shell
make format
```

| Section | Tool | Description | Configuration |
| --- | --- | --- | --- |
| backend | Ruff | Python code formatting, imports sorting  | [`backend/pyproject.toml`](./backend/pyproject.toml) |
| backend | `zpretty` | XML and ZCML formatting  | -- |
| frontend | ESLint | Fixes most common frontend issues | [`frontend/.eslintrc.js`](.frontend/.eslintrc.js) |
| frontend | prettier | Format JS and Typescript code  | [`frontend/.prettierrc`](.frontend/.prettierrc) |
| frontend | Stylelint | Format Styles (css, less, sass)  | [`frontend/.stylelintrc`](.frontend/.stylelintrc) |

Formatters can also be run within the `backend` or `frontend` folders.

### Linting the codebase
or `lint`:

 ```shell
make lint
```

| Section | Tool | Description | Configuration |
| --- | --- | --- | --- |
| backend | Ruff | Checks code formatting, imports sorting  | [`backend/pyproject.toml`](./backend/pyproject.toml) |
| backend | Pyroma | Checks Python package metadata  | -- |
| backend | check-python-versions | Checks Python version information  | -- |
| backend | `zpretty` | Checks XML and ZCML formatting  | -- |
| frontend | ESLint | Checks JS / Typescript lint | [`frontend/.eslintrc.js`](.frontend/.eslintrc.js) |
| frontend | prettier | Check JS / Typescript formatting  | [`frontend/.prettierrc`](.frontend/.prettierrc) |
| frontend | Stylelint | Check Styles (css, less, sass) formatting  | [`frontend/.stylelintrc`](.frontend/.stylelintrc) |

Linters can be run individually within the `backend` or `frontend` folders.

## Internationalization 🌐

Generate translation files for Plone and Volto with ease:

```shell
make i18n
```

## Credits and acknowledgements 🙏

This add-on is built on top of the awesome add-ons [volto-form-block](https://github.com/collective/volto-form-block) and [collective.volto.formsupport](https://github.com/collective/collective.volto.formsupport) developed by **RedTurtle Technology**.

The current version of the codebase was developed by **kitconcept GmbH** and sponsored by the **Fachhochschule Nordwestschweiz**.

Generated using [Cookieplone (2.0.0b3)](https://github.com/plone/cookieplone) and [cookieplone-templates (6678734)](https://github.com/plone/cookieplone-templates/commit/6678734cc3713f3fab9ea510616cef59dc466514) on 2026-06-10 18:43:35.112495. A special thanks to all contributors and supporters!
