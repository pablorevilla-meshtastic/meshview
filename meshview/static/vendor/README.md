# Bundled browser libraries

Meshview serves its third-party JavaScript, CSS, fonts and Leaflet marker images from
this directory. These files are included in the repository and container image;
no CDN connection or asset download is needed at application startup.

`manifest.json` records each package's pinned version, npm archive URL, archive
SHA-256 checksum, and included files. License files and ECharts' NOTICE are kept
alongside the distributions. The distributions are unmodified upstream files.

To update a library:

1. Download its versioned npm archive and verify its source and checksum.
2. Copy the required distribution files and license notices into a new versioned
   directory, preserving relative paths for CSS images and source maps.
3. Update `manifest.json` and the `/static/vendor/` references in templates and
   static HTML pages. Recalculate any `integrity` attributes from the new files.
4. Check the affected pages in a browser, including maps, charts, and QR codes,
   and remove the old version once no references remain.

All charts use ECharts 5.5.0, including pages that previously loaded an unpinned
version. Leaflet is 1.9.4, Leaflet Heat is 0.2.0, PolylineDecorator is 1.6.0,
Bootstrap is 5.3.3, and QRCode.js is 1.0.0.

The Inter typeface is bundled from `@fontsource-variable/inter` 5.3.0 (SIL Open Font
License 1.1): only the variable weight axis, normal and italic, for every subset.
Browsers download just the subsets a page uses through `unicode-range`.

Icons come from `@tabler/icons` 3.51.0 (MIT): only the SVG files the UI uses,
unmodified. `/static/icons.css` maps each one to a `.ti-<name>` class that paints
it in the current text color through a CSS mask.

Map tiles and other external data services still require network access.
