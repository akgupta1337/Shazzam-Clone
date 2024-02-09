from logic.Fingerprint import Fingerprint
import os

# Define the directory path
directory = "recorded_audios"

# Initialize an empty list to store song names with relative paths
song_list = []

# Iterate over all files in the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file has a .wav extension
        if file.endswith(".wav"):
            # Get the relative path of the file
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            # Add the relative path and file name to the list
            song_list.append(f"recorded_audios/{relative_path}")

# Print the list of song names with relative paths

song_list = ["recorded_audios/recorded_classical.wav","recorded_audios/recorded_jazz.wav","recorded_audios/recorded_pop.wav"]

engine = Fingerprint()

for song_name in song_list:
    print("----------------------------------")
    result = engine.shazzam(song_name)
    song_name = song_name.split("/")[-1]
    print(f"Processing: {song_name}")
    print("Predicted song =>",result,end='')
    print("----------------------------------\n")

