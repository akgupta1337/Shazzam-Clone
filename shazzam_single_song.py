from logic.Fingerprint import Fingerprint



engine = Fingerprint()

song_name = "recorded_audio.wav"
print("------------------------------")
print(f"SHAZZMING!: {song_name}")

identified_song = engine.shazzam(song_name)

print("Predicted song =>",identified_song)
print("------------------------------")