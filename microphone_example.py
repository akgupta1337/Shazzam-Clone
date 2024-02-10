import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from logic.Fingerprint import Fingerprint

# Parameters for recording
duration = 15  # Recording duration in seconds
sample_rate = 44100  # Sample rate (samples per second)

# Start recording
print("Recording...")
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  # Wait for the recording to finish

# Calculate the maximum amplitude
max_amplitude = np.max(np.abs(audio_data))

# Adjust the audio gain based on the maximum amplitude
target_amplitude = 3  # Set your desired maximum amplitude (adjust as needed)
scaling_factor = target_amplitude / max_amplitude
audio_data_scaled = audio_data * scaling_factor

# Save recording to a WAV file
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
