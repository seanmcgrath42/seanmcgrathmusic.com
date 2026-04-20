"""
sync.py — sync the master ChordPro directory into the Jekyll site.

Run this whenever you:
  - Add a new song (.pro file + entry in a Batch N.lst)
  - Fix lyrics in an existing song
  - Add a new batch (.lst file)

What it does:
  1. Reads all Batch N.lst files from the master directory (canonical order)
  2. Extracts the key from each .pro file
  3. Rewrites _data/songs.yml — preserving youtube_id, mp3_gdrive_id, and covers
  4. Copies all .pro files to assets/chordpro/
  5. Creates _songs/[slug].md stubs for any NEW songs (never overwrites existing ones)

What it never touches:
  - The body of any _songs/*.md file (that's where you write the story)
  - youtube_id, mp3_gdrive_id, covers values already in songs.yml
"""

import os, re, shutil, sys
from pathlib import Path

MASTER       = Path("../smg_songbook/chordpro")
SITE_CHORDPRO = Path("assets/chordpro")
SONGS_DATA   = Path("_data/songs.yml")
SONGS_DIR    = Path("_songs")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"['\u2019\u2018`]", "", s)   # strip apostrophes
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def read_key_from_pro(path: Path) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\{key:([^}]*)\}", line.strip(), re.IGNORECASE)
                if m:
                    return m.group(1).strip()
    except OSError:
        pass
    return ""


def read_batches() -> list[tuple[int, list[str]]]:
    """Return [(batch_num, [title, ...]), ...] from Batch N.lst files."""
    batches = []
    for i in range(1, 100):
        path = MASTER / f"Batch {i}.lst"
        if not path.exists():
            break
        lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        batches.append((i, lines[1:]))   # lines[0] is the "Batch N" label
    return batches


def load_existing_songs() -> dict:
    """Parse _data/songs.yml into {slug: record} preserving manual fields."""
    if not SONGS_DATA.exists():
        return {}
    # Simple manual parser — avoids pyyaml formatting side-effects on dump
    songs = {}
    current = {}
    for line in SONGS_DATA.read_text(encoding="utf-8").splitlines():
        if line.startswith("- "):
            if current.get("slug"):
                songs[current["slug"]] = current
            current = {}
            line = line[2:]
        if ":" in line and not line.startswith(" "):
            pass
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', stripped)
        if m:
            current[m.group(1)] = m.group(2)
    if current.get("slug"):
        songs[current["slug"]] = current
    return songs


def find_pro(slug: str, title: str, pro_map: dict) -> Path | None:
    """Find the .pro file for a song by slug or fuzzy title match."""
    if slug in pro_map:
        return pro_map[slug]
    # Fallback: compare lowercased, stripped titles
    target = re.sub(r"[^a-z0-9 ]", "", title.lower())
    for stem, path in pro_map.items():
        candidate = re.sub(r"[^a-z0-9 ]", "", stem.replace("_", " "))
        if candidate == target:
            return path
    return None


def write_songs_yml(songs: list[dict]) -> None:
    lines = [
        "# Master song list — batch order is canonical.",
        "# Edit youtube_id, mp3_gdrive_id, and covers here; run sync.py after adding songs.",
        "",
    ]
    for s in songs:
        covers = s.get("covers", "[]")
        if not covers or covers == "":
            covers = "[]"
        lines += [
            f"- title: \"{s['title']}\"",
            f"  slug: {s['slug']}",
            f"  batch: {s['batch']}",
            f"  batch_position: {s['batch_position']}",
            f"  youtube_id: \"{s['youtube_id']}\"",
            f"  key: \"{s['key']}\"",
            f"  mp3_gdrive_id: \"{s['mp3_gdrive_id']}\"",
            f"  covers: {covers}",
            "",
        ]
    SONGS_DATA.write_text("\n".join(lines), encoding="utf-8")


def write_stub(path: Path, slug: str) -> None:
    path.write_text(
        f"---\nlayout: song\nslug: {slug}\n---\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not MASTER.exists():
        sys.exit(f"ERROR: master directory not found: {MASTER.resolve()}")

    SITE_CHORDPRO.mkdir(parents=True, exist_ok=True)
    SONGS_DIR.mkdir(parents=True, exist_ok=True)

    batches  = read_batches()
    existing = load_existing_songs()
    pro_map  = {p.stem: p for p in MASTER.glob("*.pro")}

    # --- Build updated song list -------------------------------------------
    updated: list[dict] = []
    new_songs: list[str] = []

    for batch_num, titles in batches:
        for pos, title in enumerate(titles, 1):
            slug    = slugify(title)
            pro     = find_pro(slug, title, pro_map)
            key     = read_key_from_pro(pro) if pro else ""
            old     = existing.get(slug, {})

            updated.append({
                "title":          title,
                "slug":           slug,
                "batch":          batch_num,
                "batch_position": pos,
                "youtube_id":     old.get("youtube_id", ""),
                "key":            key or old.get("key", ""),
                "mp3_gdrive_id":  old.get("mp3_gdrive_id", ""),
                "covers":         old.get("covers", "[]"),
            })
            if slug not in existing:
                new_songs.append(title)

    write_songs_yml(updated)
    print(f"  _data/songs.yml  — {len(updated)} songs written.")

    # --- Copy .pro files ---------------------------------------------------
    copied = 0
    for src in MASTER.glob("*.pro"):
        shutil.copy2(src, SITE_CHORDPRO / src.name)
        copied += 1
    print(f"  assets/chordpro/ — {copied} .pro files synced.")

    # --- Create stubs for new songs only -----------------------------------
    stubs_created = 0
    for song in updated:
        stub = SONGS_DIR / f"{song['slug']}.md"
        if not stub.exists():
            write_stub(stub, song["slug"])
            stubs_created += 1

    if new_songs:
        print(f"  _songs/          — {stubs_created} new stub(s): {', '.join(new_songs)}")
    else:
        print(f"  _songs/          — no new songs.")

    print("Sync complete.")


if __name__ == "__main__":
    main()
