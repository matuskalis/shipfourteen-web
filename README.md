# shipfourteen.com

Static site. One `index.html`, no build step, no framework.

## Deploy

```bash
npx vercel deploy --prod --yes
```

Vercel project: `shipfourteen-web` (team `m3kalis-3804's projects`).
Serves `shipfourteen.com`; `www` 308-redirects to the apex.

## Local

```bash
python3 -m http.server 4317
```

`file://` will not work — the ES module import map needs a real origin.

## Layout

```
index.html              everything: markup, CSS, the three.js scene
vendor/                 three.module.js + OrbitControls.js, pinned to r169
fonts/                  Inter, variable, subset to the glyphs the page uses
assets/moon-*.webp      NASA colour + elevation maps, see assets/CREDITS.md
assets/work-*.webp      portfolio screenshots, 640x400
assets/og.jpg           social card, regenerate after hero changes
```

## Things that will bite you

- **The fonts are subsets.** `inter-latin.woff2` covers ASCII, Latin-1 and a
  short list of punctuation; `inter-latin-ext.woff2` holds only `Š` and `š`.
  Add copy with a character outside those and it silently falls back to the
  system font. Re-subset with `pyftsubset` and widen the `unicode-range`.
- **Google serves one variable file for every weight.** Do not download four.
  The `@font-face` rules declare `font-weight: 300 600` and the `wght` axis
  does the rest.
- **three.js loads in `requestIdleCallback`,** so the planet appears after the
  text. That is deliberate: it keeps 263 KB out of the first paint.
- **The hero column spans the full width** for layout, so it carries
  `pointer-events: none` with `auto` on its children. Without that it covers
  the canvas and the planet stops responding to the mouse.
- **`resize()` checks `window.innerWidth`, not the canvas width.** The canvas
  is 62% of the viewport, so a canvas-width check silently puts desktop into
  the mobile branch.
- **The 3D scene has one shader loop over asteroids,** capped at
  `INFLUENCE_COUNT = 24`. The asteroid array is sorted biggest-first, so the
  first 24 are the ones worth simulating. Raising it costs
  `particleCount * INFLUENCE_COUNT` vertex iterations per frame.

## Regenerating the OG card

```bash
python3 -m http.server 4317
# screenshot the hero at 1200x630, then:
sips -s format jpeg -s formatOptions 82 og-raw.png --out assets/og.jpg
```

## Previous site

The AI Feature Sprint site is still deployed at `shipfourteen-site.vercel.app`
(project `shipfourteen-site`). It no longer holds the apex domain.
