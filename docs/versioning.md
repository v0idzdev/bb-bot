# ⚙️ Versioning

This is a guide explaining our versioning system, which may help developers better understand how we make releases, and where their changes will end up.
<br><br>

## 🔧 Stable Releases

Stable releases are created from the **master** branch. We use **[semantic versioning](https://semver.org/)** to indicate the types of changes present in each new release.

- **Major versions**

When we release a new major version, it indicates a **large, breaking change** to the way the bot works. This can be due to a rewrite, removal of a major feature, or otherwise.

- **Minor versions**

When we release a minor version, it means we've **added a new feature**. This can be a small feature such as a new UI for a command, or it can be a large change/feature.

- **Patch versions**

When we release a patch version, it means we've fixed an issue with an **existing feature**, without changing the way it works/what the user interacts with besides minor UI changes for usability.
<br><br>

## 🔨 Development Releases

Development releases are created from the **dev** branch. Usually, we don't create a development version of a release if it's a patch version.

- **Alpha/beta versions**

We use `-alpha.x` for **development** releases in which new features may be **added/removed at any time**, and where the code is **not considered stable**. Alpha releases usually involve **developing new features**.

We use `beta.x` for **development** releases in which new features are **unlikely to be added**, and where the code is **partially stable**. Beta releases usually involve **bug fixing** and **performance improvements**.

- **Release candidate versions**

We use `-rc.x` for **development** releases in which the code in **mostly stable**, and where new features will **not be added**. Release candidate versions usually involve **minor tweaks** and **code refactoring**.
