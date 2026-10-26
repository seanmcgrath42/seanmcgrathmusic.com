"""
Fetches MP3 file IDs from a public Google Drive folder and populates
mp3_gdrive_id in _data/songs.yml by matching on song title.

Usage:
    python populate_mp3_ids.py YOUR_API_KEY
"""

import sys
import re
import requests
import yaml

FOLDER_ID = "16FXjFzthxCSRujDDvgKtySm-kM_4ccMd"
SONGS_YML  = "_data/songs.yml"

def normalise(s):
    """Lowercase, strip punctuation and extra spaces for fuzzy matching."""
    s = s.lower()
    s = re.sub(r"['''\-]", " ", s)      # apostrophes, hyphens → space
    s = re.sub(r"[^a-z0-9 ]", "", s)    # strip everything else
    s = re.sub(r"\s+", " ", s).strip()
    return s

def fetch_drive_files(api_key):
    files = []
    url = "https://www.googleapis.com/drive/v3/files"
    params = {
        "q": f"'{FOLDER_ID}' in parents and trashed = false and name contains '.mp3'",
        "fields": "nextPageToken, files(id, name)",
        "pageSize": 200,
        "key": api_key,
    }
    while True:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        files.extend(data.get("files", []))
        token = data.get("nextPageToken")
        if not token:
            break
        params["pageToken"] = token
    return files

def main():
    if len(sys.argv) < 2:
        print("Usage: python populate_mp3_ids.py YOUR_API_KEY")
        sys.exit(1)

    api_key = sys.argv[1]

    print("Fetching files from Google Drive...")
    drive_files = fetch_drive_files(api_key)
    print(f"Found {len(drive_files)} files in folder.")

    # Build lookup: normalised title → file ID
    drive_map = {}
    for f in drive_files:
        name = f["name"]
        # Strip extension
        title = re.sub(r'\.(mp3|wav|m4a|flac)$', '', name, flags=re.IGNORECASE)
        drive_map[normalise(title)] = f["id"]

    with open(SONGS_YML, "r", encoding="utf-8") as fh:
        songs = yaml.safe_load(fh)

    matched = 0
    unmatched = []

    for song in songs:
        key = normalise(song.get("title", ""))
        if key in drive_map:
            song["mp3_gdrive_id"] = drive_map[key]
            matched += 1
        else:
            unmatched.append(song["title"])

    with open(SONGS_YML, "w", encoding="utf-8") as fh:
        yaml.dump(songs, fh, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"\nOK Matched and updated: {matched} songs")
    if unmatched:
        print(f"\nMISSING No Drive file found for {len(unmatched)} songs:")
        for t in unmatched:
            print(f"   - {t}")
    else:
        print("OK All songs matched.")

if __name__ == "__main__":
    main()
