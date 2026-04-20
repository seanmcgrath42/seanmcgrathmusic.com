# seanmcgrathmusic.com — Development Journal

---

## Session 1 — 2026-04-20

### Background & Goals

Sean McGrath is an Irish folk singer/songwriter with 90 original songs, all released under a
Creative Commons Attribution 4.0 (CC BY) licence. The site has two audiences:

- **Fans** — who want to know the story behind each song
- **Musicians** — who want everything they need to record their own version: chords, lyrics,
  ChordPro file, MP3, and eventually a place to see other people's covers

The site is personal and non-commercial. Sean does not perform live at present, is not
monetising his YouTube channel, and is not selling anything. The aesthetic goal was described
as "chill and folky — not hustling anything."

### Design Decisions

- **Light background**, warm off-white palette, serif headings (Lora), clean sans body (Source
  Sans 3). Muted sage green as the accent colour.
- **Jekyll** hosted on GitHub Pages, building automatically on push. No Node, no framework.
- **Song catalog** browsable two ways: by Batch (canonical order) and Alphabetically.
- **Song pages** have a clear split: "The Story" section (fan-facing) and "For Musicians"
  section (chords, downloads). A "Versions & Covers" section will grow over time as YouTube
  embeds are added.
- **ChordPro rendered client-side** in JavaScript — no Ruby/Liquid parsing needed.
- **MP3s** to be hosted on Google Drive (free, no repo bloat). Drive file IDs go in
  `_data/songs.yml`.
- A **full songbook PDF** will be added to `assets/` when ready.

### Source of Truth

The master ChordPro directory lives at `../smg_songbook/chordpro/` (outside this repo).
Running `python sync.py` from the site root:
1. Reads all `Batch N.lst` files to get canonical song order
2. Extracts keys from `.pro` files
3. Rewrites `_data/songs.yml` — preserving YouTube IDs, MP3 Drive IDs, and covers
4. Copies all `.pro` files to `assets/chordpro/`
5. Creates `_songs/[slug].md` stubs for any new songs (never overwrites existing ones)

Song stubs are intentionally minimal — just `layout: song` and `slug`. The song body is
reserved for the story text (written in Markdown). All structured data lives in `songs.yml`.

### Data Gathered

- All 90 song titles and their batch assignments read from `Batch 1–9.lst`
- All 90 YouTube video IDs fetched automatically from the `@seanmcgrathmusic` channel
  via the YouTube API
- Keys extracted from `.pro` files where present (many songs do not have a `{key:}` tag)

### What Was Built

| File / Folder | Purpose |
|---|---|
| `_config.yml` | Jekyll config, collection setup, custom domain |
| `_data/songs.yml` | All 90 songs: batch, position, YouTube ID, key, MP3 ID |
| `_layouts/default.html` | Base page layout |
| `_layouts/song.html` | Song page — looks up data from `songs.yml` by `page.slug` |
| `_includes/head.html` | `<head>` with Google Fonts, SEO tag, correct page title |
| `_includes/header.html` | Site nav: Songs / About / YouTube |
| `_includes/footer.html` | CC BY licence notice |
| `assets/css/main.scss` | Full warm-folk stylesheet |
| `assets/js/chordpro.js` | Client-side ChordPro renderer |
| `index.html` | Home page with intro and Batch 9 preview |
| `songs/index.html` | Catalog with Batch / Alpha toggle |
| `about/index.html` | Bio placeholder + CC licence explanation |
| `_songs/*.md` | 90 minimal song stubs (story body empty, to be filled) |
| `assets/chordpro/*.pro` | 90 ChordPro files (synced from master directory) |
| `sync.py` | Master sync script |
| `PREVIEW.md` | Local preview instructions |

### ChordPro Rendering

The JavaScript renderer handles:
- `{title:}` — renders as a bold heading at the top of the chart, followed by "by @seanmcgrathmusic"
- `{key:}` — skipped (shown in the song meta line instead)
- `{comment:label}` — renders as small italic muted text above a section
- `{soc}` / `{eoc}` — wraps chorus content in a left-bordered block (green accent bar)
- `{chorus}` — renders a "Chorus" repeat marker
- `[Chord]lyric` lines — chords rendered above their lyrics in monospace, with `column-gap` spacing
- Blank lines — verse breaks

### Bugs Fixed

- **404 on song pages**: Jekyll converts underscores to hyphens in permalink `:name`, so
  `be_here_soon.md` → `/songs/be-here-soon/`. Fixed by adding `| replace: '_', '-'` to all
  slug-to-URL conversions in templates.
- **Duplicate `<title>` tag**: `jekyll-seo-tag` was generating its own title alongside the
  explicit one. Fixed with `{% seo title=false %}`.
- **Liquid syntax error in prev/next nav**: `all_songs[index | minus: 1]` is invalid Liquid.
  Fixed by pre-assigning `{% assign prev_index = current_index | minus: 1 %}`.
- **Chords running together** (e.g. `AmDmAmE7Am`): consecutive chords with no lyric text had
  no visual separation. Fixed with `column-gap: 0.35rem` on `.chord-line`.
- **Duplicate Gemfile entry** for `jekyll-seo-tag`. Cleaned up.

### Repository

- GitHub: https://github.com/seanmcgrath42/seanmcgrathmusic.com
- Branch: `master`
- Initial commit pushed: 2026-04-20

### Outstanding TODOs

- [ ] Enable GitHub Pages (Settings → Pages → Deploy from branch → master → / (root))
- [ ] Make it easy to print a single song without page chrome (header, footer, nav)
- [ ] Test on mobile
- [ ] Remove the Key column from the By Batch browse view
- [ ] Write song stories (90 × `_songs/[slug].md` body text)
- [ ] Add bio text to `about/index.html`
- [ ] Add Google Drive MP3 IDs to `_data/songs.yml` for each song
- [ ] Add the songbook PDF to `assets/` and set `songbook_pdf:` in `_config.yml`
- [ ] Add photos to `assets/images/`
