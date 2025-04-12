import os
import re
import shutil
import random


import os
import random
import sys
from pathlib import Path, PurePath



frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
    print("cd into", os.path.dirname(sys.executable))
    os.chdir(os.path.dirname(sys.executable))
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    print("cd into", bundle_dir)
    os.chdir(bundle_dir)

print('we are', frozen, 'frozen')
print('bundle dir is', bundle_dir)
print('sys.argv[0] is', sys.argv[0])
print('sys.executable is', sys.executable)
print('os.getcwd is', os.getcwd())


# === Configuration ===
INPUT_PLAYLIST_DIR = "input_playlist"
EXTRA_SONGS_DIR = "./"
OUTPUT_BASE_DIR = "final_playlist"

GENRE_MAP = {"B": "bachata", "S": "salsa", "K": "kizomba"}
REVERSE_GENRE = {v: k for k, v in GENRE_MAP.items()}

PATTERNS = {
    "b3s2k3": {"bachata": 3, "salsa": 2, "kizomba": 3},
    "b3s1": {"bachata": 3, "salsa": 1},
    "b3s2": {"bachata": 3, "salsa": 2}
}

# === Helpers ===

def parse_input_playlist(folder):
    songs = {"bachata": [], "salsa": [], "kizomba": []}
    seen = set()
    for fname in os.listdir(folder):
        full_path = os.path.join(folder, fname)
        if not os.path.isfile(full_path):
            continue
        match = re.match(r"^\d{1,3}([BSK])\s+(.+)", fname)
        if match:
            letter, name = match.groups()
            genre = GENRE_MAP.get(letter)
            if genre and name.lower() not in seen:
                seen.add(name.lower())
                songs[genre].append((name.strip(), full_path))
    return songs

def parse_genre_folder(genre_folder):
    songs = []
    seen = set()
    for fname in os.listdir(genre_folder):
        full_path = os.path.join(genre_folder, fname)
        if os.path.isfile(full_path):
            name = fname.strip()
            if name.lower() not in seen:
                seen.add(name.lower())
                songs.append((name, full_path))
    return songs

def merge_sources(primary, extras):
    merged = {"bachata": [], "salsa": [], "kizomba": []}
    seen = set()
    for genre in merged:
        all_songs = primary.get(genre, []) + extras.get(genre, [])
        for name, path in all_songs:
            if name.lower() not in seen:
                merged[genre].append((name, path))
                seen.add(name.lower())
        random.shuffle(merged[genre])
    return merged

def create_pattern_playlist(pattern_name, pattern_counts, all_songs):
    output_dir = os.path.join(OUTPUT_BASE_DIR, pattern_name)
    os.makedirs(output_dir, exist_ok=True)
    playlist_entries = []
    index = 1
    local_songs = {g: all_songs[g][:] for g in all_songs}  # copy to avoid shared depletion

    while True:
        current_block = []
        for genre, count in pattern_counts.items():
            if len(local_songs[genre]) < count:
                return playlist_entries
            current_block += [(genre, local_songs[genre].pop(0)) for _ in range(count)]

        for genre, (name, path) in current_block:
            number = f"{index:03d}"
            letter = REVERSE_GENRE[genre]
            new_name = f"{number}{letter} {name}"
            dst_path = os.path.join(output_dir, new_name)
            shutil.copy2(path, dst_path)
            playlist_entries.append(new_name)
            index += 1

def write_m3u(playlist_entries, pattern_name):
    m3u_path = os.path.join(OUTPUT_BASE_DIR, f'{pattern_name}.m3u')
    with open(m3u_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in playlist_entries:
            match = re.match(r"^\d{1,3}([BSK])\s+(.+)", entry)
            if match:
                letter, name = match.groups()
                genre = GENRE_MAP.get(letter)
                f.write(f"#EXTINF:-1,{name}\n")
            f.write(f"{pattern_name}/{entry}\n")

# === Main ===

def main():
    print("🎵 Loading input playlist...")
    input_songs = parse_input_playlist(INPUT_PLAYLIST_DIR)

    print("🎵 Loading extra songs...")
    extra_songs = {
        "bachata": parse_genre_folder(os.path.join(EXTRA_SONGS_DIR, "bachata")),
        "salsa": parse_genre_folder(os.path.join(EXTRA_SONGS_DIR, "salsa")),
        "kizomba": parse_genre_folder(os.path.join(EXTRA_SONGS_DIR, "kizomba")),
    }

    print("🎵 Merging and shuffling songs...")
    all_songs = merge_sources(input_songs, extra_songs)

    for pattern_name, pattern in PATTERNS.items():
        print(f"🎶 Generating playlist: {pattern_name}")
        playlist = create_pattern_playlist(pattern_name, pattern, all_songs)
        write_m3u(playlist, pattern_name)

    print("✅ All playlists created in:", OUTPUT_BASE_DIR)

if __name__ == "__main__":
    main()
