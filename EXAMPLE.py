from logic.Shazzam import Shazzam

engine = Shazzam()

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile


# duration = 15   #set song duration
# sample_rate = 44100  

# print("Recording...")
# audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
# sd.wait()  

# max_amplitude = np.max(np.abs(audio_data))

# target_amplitude = 2.5   #set amplification as per your choice
# scaling_factor = target_amplitude / max_amplitude
# audio_data_scaled = audio_data * scaling_factor

# filename = "rec.wav"

# wavfile.write(filename, sample_rate, audio_data_scaled)

# print(f"Recording saved as {filename}")
engine.add_songs()
engine.match_song('pe.wav')
