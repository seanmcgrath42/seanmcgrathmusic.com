# Local Preview

## One-time setup

1. Download and install **Ruby+Devkit** from https://rubyinstaller.org/downloads/
   - Choose the latest `Ruby+Devkit x64` version
   - At the end of the installer, run the `ridk install` step (option 3 when prompted)

2. Open a new terminal in this folder and run:
   ```
   gem install bundler
   bundle install
   ```

## Preview the site

```
bundle exec jekyll serve
```

Then open http://localhost:4000 in your browser.

Jekyll watches for changes and rebuilds automatically. The one exception is
`_data/songs.yml` — after running `sync.py` you need to restart the server
(`Ctrl+C`, then `bundle exec jekyll serve` again).

## Adding a new song

1. Write the `.pro` file and add it to the master ChordPro directory
2. Add the song title to the correct `Batch N.lst` file in the master directory
3. Run `python sync.py` from this folder
4. Open `_songs/[new_slug].md` and write the story below the front matter
5. Add the YouTube ID and Google Drive MP3 ID to `_data/songs.yml`

## Adding a song story

Open `_songs/[slug].md` and write Markdown below the `---` line. Example:

```markdown
---
layout: song
slug: be_here_soon
---

This one started on a wet Tuesday in Cork. I had been reading about...
```

## Adding covers / other versions

In `_data/songs.yml`, find the song and edit its `covers:` field:

```yaml
covers:
  - youtube_id: "xXxXxXxXxXx"
    label: "Cover by Jane Smith, 2025"
  - youtube_id: "yYyYyYyYyYy"
    label: "Live version — Skibbereen, 2026"
```

## Adding MP3 downloads

1. Upload the MP3 to Google Drive and set sharing to "Anyone with the link"
2. Copy the file ID from the share URL (the long string between `/d/` and `/view`)
3. Paste it into `mp3_gdrive_id:` for that song in `_data/songs.yml`
