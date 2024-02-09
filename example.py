from logic.Fingerprint import Fingerprint

file_name = ["recorded_audios/recorded_classical.wav","recorded_audios/recorded_jazz.wav","recorded_audios/recorded_pop.wav"]

engine = Fingerprint()

for song_name in file_name:
    print("----------------------------------")
    result = engine.shazzam(song_name)
    song_name = song_name.split("/")[-1]
    print(f"Processing: {song_name}")
    print("Predicted song =>",result,end='')
    print("----------------------------------\n")

