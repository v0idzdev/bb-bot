# ⚙️ Versioning

This is a guide explaining our versioning system, which may help developers better understand how we make releases, and where their changes will end up.

## 🔧 Stable Releases

Stable releases are created from the **master** branch. We use **[semantic versioning](https://semver.org/)** to indicate the types of changes present in each new release.

- **Major versions**

When we release a new major version, it indicates a **large, breaking change** to the way the bot works. This can be due to a rewrite, removal of a major feature, or otherwise.

- **Minor versions**

When we release a minor version, it means we've **added a new feature**. This can be a small feature such as a new UI for a command, or it can be a large change/feature.

- **Patch versions**

When we release a patch version, it means we've fixed an issue with an **existing feature**, without changing the way it works/what the user interacts with.

## 🔨 Development Releases

Development releases are created from the **dev** branch. Usually, we don't create a development version of a release if it's a patch version.

- **Release candidate versions**

Release candidate versions include an additional `-rc.x` at the end of the version name. We use release candidate versions to denote a **development** version.

- **Alpha/beta versions**

We do not use `-alpha.x` or `beta.x` releases - we use `-rc.x` for all **pre-releases** to keep versioning simple.
