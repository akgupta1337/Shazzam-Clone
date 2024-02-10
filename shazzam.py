from logic.Fingerprint import Fingerprint


engine = Fingerprint()

song_name = "path.wav"
print(f"Processing: {song_name}")

result = engine.shazzam(song_name)

print(result)