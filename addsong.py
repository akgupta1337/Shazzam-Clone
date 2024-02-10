from logic.Fingerprint import Fingerprint
import os

directory = "original_audios"

song_list = []

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".wav"):
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            song_list.append(f"original_audios/{relative_path}")

engine = Fingerprint()

for song in song_list:
    engine.add_song(song)