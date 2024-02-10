import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from logic.Fingerprint import Fingerprint

'''
For recording audio from microphone and then SHAZAAMING IT!
IMPORTANT: RECORD IN SILENCE AND MAKE SURE THERE IS NO NOISE!
'''
duration = 15
sample_rate = 44100  

print("Recording...")
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  

max_amplitude = np.max(np.abs(audio_data))

target_amplitude = 1.5
scaling_factor = target_amplitude / max_amplitude
audio_data_scaled = audio_data * scaling_factor

filename = "recorded_audio.wav"

wavfile.write(filename, sample_rate, audio_data_scaled)

print(f"Recording saved as {filename}")



engine = Fingerprint()

song_name = "recorded_audio.wav"
print("------------------------------")
print(f"SHAZZMING!: {song_name}")

identified_song = engine.shazzam(song_name)

print("Predicted song =>",identified_song)
print("------------------------------")
