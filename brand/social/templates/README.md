# Post templates

Drop-in, on-brand post/thumbnail templates. Both are self-contained SVGs using the
kit's emblem, palette (deep-navy ground, emerald `#E8B44A` accent), and Avenir Next.

| File | Size | Use |
|---|---|---|
| `shipvane-post-square-1080.svg` | 1080×1080 | Instagram / feed announcements |
| `shipvane-post-landscape-1200x675.svg` | 1200×675 (16:9) | X posts, link cards, YouTube thumbnails |

## Editing

Each editable string is marked with an `<!-- EDIT: … -->` comment — swap the text in
the following `<text>`/`<tspan>`:

- **eyebrow** — the uppercase emerald label (keep it short, `letter-spacing` is set)
- **headline** — the big white line(s); keep to the line count shown so it doesn't collide
- **subline** — the light-blue supporting line

Keep emerald for accents only; keep the wordmark two-tone (`ship` white / `vane` emerald).

## Re-rendering to PNG

Fonts render in real Avenir Next on macOS. Regenerate PNGs with the sibling script:

```bash
../render.sh              # renders every SVG under brand/social to a matching PNG
```
