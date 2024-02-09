from Fingerprint import Fingerprint

file_name = ["recorded_classical.wav","recorded_jazz.wav","recorded_pop.wav"]

engine = Fingerprint()

for song_name in file_name:
    print("----------------------------------")
    print(f"Processing: {song_name}")
    result = engine.shazzam(song_name)
    print("Predicted song =>",result,end='')
    print("----------------------------------\n")
