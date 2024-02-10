from logic.Fingerprint import Fingerprint
import os


'''
This example is if you have a list of recorded songs in the folder 
recorded_audios and you want SHAZZAM ALL OF THEM
'''
directory = "recorded_audios"

song_list = []

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".wav"):
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            song_list.append(f"recorded_audios/{relative_path}")



engine = Fingerprint()

for song_name in song_list:
    print("----------------------------------")
    result = engine.shazzam(song_name)
    song_name = song_name.split("/")[-1]
    print(f"Processing: {song_name}")
    print("Predicted song =>",result,end='')
    print("----------------------------------\n")

