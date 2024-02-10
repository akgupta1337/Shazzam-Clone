import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from logic.Fingerprint import Fingerprint

'''
For recording audio from microphone and then SHAZAAMING IT!
'''
duration = 15  
sample_rate = 44100  

print("Recording...")
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  

max_amplitude = np.max(np.abs(audio_data))

target_amplitude = 3  
scaling_factor = target_amplitude / max_amplitude
audio_data_scaled = audio_data * scaling_factor

filename = "recorded_audio.wav"

wavfile.write(filename, sample_rate, audio_data_scaled)

print(f"Recording saved as {filename}")



engine = Fingerprint()

song_name = "recorded_audio.wav"
print("------------------------------")
print(f"Processing: {song_name}")

result = engine.shazzam(song_name)

print("Predicted song =>",result)
print("------------------------------")
