# Translating Meshview

Set `[site] language` in `config.ini` to `en`, `es`, or `ru`, then restart the web
server and reload the page. Language catalogs live in `meshview/lang/`.

The `ui` section uses the English source text as its key. Add the same key to
all three catalogs, with English, Spanish, and Russian values respectively.
Keep named placeholders such as `{count}` unchanged; their order can differ.
Missing keys fall back to English. Existing page-specific sections remain
supported and also receive English defaults through `/api/lang`.

## Templates and scripts

For fixed template text or attributes, use Jinja's `tr` helper. Jinja escapes the
translated result automatically:

```html
<h1>{{ tr("Reliability") }}</h1>
<input placeholder="{{ tr('Search node...') }}">
```

Template pages embed their configured UI catalog before loading page scripts.
For generated text, use the shared helper:

```javascript
status.textContent = MeshI18n.t("Total: {count}", {count});
```

When composing HTML, use `MeshI18n.h` to escape both the translated string and
its interpolated values:

```javascript
popup.innerHTML = `<b>${MeshI18n.h("Node {id}", {id: node.node_id})}</b>`;
```

Pass application copy to these helpers. Do not pass packet payloads, device
names, channel names, firmware identifiers, or protocol enum values as keys.
Use `MeshI18n.language` when formatting dates and numbers for the UI.

Standalone static pages load `/static/i18n.js` and mark fixed copy explicitly:

```html
<button data-i18n="Refresh">Refresh</button>
<input data-i18n-placeholder="Search node..." placeholder="Search node...">
```

`data-i18n-title` and `data-i18n-aria-label` translate their respective attributes.
Before generating dynamic content on a standalone page, await
`MeshI18n.ready`. English text remains usable if the language request fails.
Only marked elements are changed; network content is never translated by a
DOM observer.

## API reference

Edit `docs/API_Documentation.md` and run:

```sh
node scripts/build-api-docs.mjs
```

The builder marks prose fragments for translation while preserving code
examples and endpoint identifiers. Add new prose keys to the three `ui`
catalogs after regenerating. Do not hand-edit the generated `static/api.html`.

## Validation

```sh
env/bin/python -m pytest -q
node --test tests/i18n.test.cjs
```

The catalog tests check duplicate keys, language coverage, placeholder parity,
UI source keys, template rendering, and English fallback. The JavaScript tests
check interpolation, escaping, static-page loading, preservation of unmarked
content, and sort indicators.
