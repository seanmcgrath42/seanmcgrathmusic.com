# seanmcgrathmusic.com

Personal website for Sean McGrath — Irish folk singer/songwriter. 90 original songs, all released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Built with Jekyll, hosted on GitHub Pages.

---

## Local Development

```bash
cd seanmcgrathmusic_website
bundle exec jekyll serve --watch
```

Site runs at `http://localhost:4000`. Note: changes to `_config.yml` require a server restart to take effect.

---

## How to Add / Update Content

### Add a song story

Edit the corresponding file in `_songs/[slug].md`. The front matter is minimal — just write the story in Markdown below the `---`:

```markdown
---
layout: song
slug: woe_is_me
---

This song was written on a rainy Tuesday in Galway...
```

The "The Story" heading on the song page only appears when there is content here.

### Add a YouTube video to a song

Edit `_data/songs.yml` and set the `youtube_id` field for the song:

```yaml
- slug: woe_is_me
  youtube_id: dQw4w9WgXcQ
```

### Add an MP3 download to a song

1. Upload the MP3 to Google Drive and get the file ID from the share URL
2. Edit `_data/songs.yml` and set `mp3_gdrive_id` for that song:

```yaml
- slug: woe_is_me
  mp3_gdrive_id: 1A2B3C4D5E6F7G8H
```

The MP3 download button is hidden on the song page until this is set.

### Add a cover / other version to a song

Edit `_data/songs.yml` and add to the `covers` list for that song:

```yaml
- slug: woe_is_me
  covers:
    - youtube_id: dQw4w9WgXcQ
      label: "Cover by Mary Murphy"
```

### Replace the dummy Songbook PDF

Drop the real `songbook.pdf` into `assets/` — it replaces the placeholder automatically. The filename is set in `_config.yml` under `songbook_pdf`.

### Replace the dummy Songbook ChordPro

Drop the real `songbook.pro` into `assets/` — it replaces the placeholder automatically.

### Add MP3 zip downloads (home page)

Upload zip files to Google Drive and paste the file IDs into `_data/mp3_zips.yml`:

```yaml
all_gdrive_id: "1A2B3C4D5E6F7G8H"   # zip of all 90 songs

batches:
  - batch: 1
    gdrive_id: "1A2B3C4D5E6F..."     # zip of Batch 1 (10 songs)
  - batch: 2
    gdrive_id: ""                    # leave empty to hide
  ...
```

The entire "Download MP3s" section on the home page is hidden until at least one ID is set. Individual batch links are hidden until their ID is set.

**Getting a Google Drive file ID:** share the file (anyone with link), then copy the ID from the URL:
`https://drive.google.com/file/d/`**`THIS_PART`**`/view`

### Add a background paper texture

Drop `paper-texture.jpg` into `assets/images/`. The body background CSS is already wired up to use it.

### Add songs from a new batch

Run the sync script from the site root:

```bash
python sync.py
```

This reads the master ChordPro directory at `../smg_songbook/chordpro/`, updates `_data/songs.yml`, copies `.pro` files to `assets/chordpro/`, and creates stubs in `_songs/` for any new songs. Existing song stubs (with story content) are never overwritten.

---

## Pages You Can Edit

These are the content files you'll touch most often. All use Markdown.

| File | What it controls |
|---|---|
| `index.html` | Home page — intro text, tagline, CTA buttons, social links |
| `about/index.html` | About / bio page |
| `_songs/[slug].md` | Story text for an individual song (body below the `---`) |

### Home page (`index.html`)

The intro paragraph, tagline, and body text are plain HTML/Markdown inside the file. Edit them directly. The CTA buttons and social links are also in this file if you need to add or reorder them.

### Bio page (`about/index.html`)

Currently a placeholder. Write your bio here in plain Markdown/HTML. There is no separate data file for this — just edit the file directly.

### Song stories (`_songs/[slug].md`)

One file per song. The slug matches the song title with spaces replaced by underscores, e.g. `_songs/woe_is_me.md`. Write the story in Markdown below the front matter:

```markdown
---
layout: song
slug: woe_is_me
---

This song came from a conversation I had in Galway in 2019...
```

The "The Story" heading on the song page only appears when there is content here — empty files show nothing.

---

## File Structure

| Path | Purpose |
|---|---|
| `_data/songs.yml` | All song metadata: batch, YouTube ID, MP3 Drive ID, key, covers |
| `_data/mp3_zips.yml` | Google Drive IDs for bulk MP3 zip downloads |
| `_songs/[slug].md` | Per-song story text (Markdown body) |
| `assets/chordpro/[slug].pro` | ChordPro files (synced from master directory) |
| `assets/mp3/.gitkeep` | Placeholder — MP3s are served via Google Drive, not committed |
| `assets/images/` | Photos and background textures |
| `assets/songbook.pdf` | Full songbook PDF (replace dummy with real file) |
| `assets/songbook.pro` | Full songbook ChordPro (replace dummy with real file) |
| `_layouts/song.html` | Song page template |
| `assets/js/chordpro.js` | Client-side ChordPro renderer |
| `assets/css/main.scss` | Site stylesheet |
| `sync.py` | Master sync script |
