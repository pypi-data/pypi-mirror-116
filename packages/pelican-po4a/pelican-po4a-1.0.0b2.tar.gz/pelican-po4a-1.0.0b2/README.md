pelican-po4a: Pelican plugin for managing l10n with po4a
========================================================

<!-- [![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/po4a/build)](https://github.com/pelican-plugins/po4a/actions) -->
[![PyPI Version](https://img.shields.io/pypi/v/pelican-po4a)](https://pypi.org/project/pelican-po4a/)
![License](https://img.shields.io/pypi/l/pelican-po4a?color=blue)

Pelican plugin for managing l10n with po4a

Features and limitations
------------------------

This plugin is intended to help with integrating [po4a](https://po4a.org) into the Pelican
build process. With po4a, it is possible to translate entire content files using any gettext
tool, e.g. [Weblate](https://weblate.org).

The plugin does the following:

 * Track content files and their translation counterparts to build the
   source/translation list in `po4a.conf`
 * Support the generic `$lang` pattern for po4a.conf source/translation sets
 * Write a `po4a.conf` file matching Pelican settings and content
 * Update message catalogs based on source files
 * Update translations based on message catalogs

The plugin supports the following other plugins:

 * [i18n_subsites](https://github.com/getpelican/pelican-plugins/tree/master/i18n_subsites) –
   the po4a plugin only acts on the main language and writes data once
 * [jinja2content](https://github.com/getpelican/pelican-plugins/tree/master/jinja2content) –
   the wrapped readers are detected for content format detection
 * [asciidoc_readers](https://github.com/getpelican/pelican-plugins/tree/master/asciidoc_reader) –
   reader is supported and detected for content format detection

Currently, the plugin has the following limitations:

 * If anything changed (source content for main language or translations), the build has
   to be run twice (a `CRITICAL` message is emitted to notify the user). This is because
   we have no control over the order in which languages are built, and translated sites (
   when using `i18n_subsites`) might be built before translations are picked up
 * `jinja2content` blocks and vanilla HTML blocks in Markdown are not handled by po4a,
   they are added to the catalogs verbatim

Patches welcome!

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-po4a

After doing that, append `po4a` to your `PLUGINS` setting.

Obviously, you also need to have `po4a` itself installed.

Usage
-----

The following settings are available:

| Setting              | Description                                    | Default                           |
|----------------------|------------------------------------------------|-----------------------------------|
| `PO4A_CONF`          | (Relative) path to `po4a.conf` file            | `./po4a.conf`                     |
| `PO4A_PO_DIR`        | (Relative) path to the catalog directory       | `./po`                            |
| `PO4A_CATALOG`       | Name of the message catalog                    | `pelican-website`                 |
| `PO4A_PAGE_PATTERN`  | Generic pattern for translation paths of pages | `content/pages/{lang}/{relpath}`  |
| `PO4A_POST_PATTERN`  | Generic pattern for translation paths of posts | `content/posts/{lang}/{relpath}`  |

All necessary po4a actions are automatically taken when building the main site language.
If changes were made, a `CRITICAL` message is logged, and starting the build again is required
(cf. limitations).

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://edugit.org/Teckids/team-pr/pelican-po4a/-/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the Apache-2.0 license.
