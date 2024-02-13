import pyaudio
import wave
from pydub import AudioSegment
import os

def record_audio(filename, duration=10):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording audio...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Recording finished")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(f"{filename}.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    convert_to_mp3(f"{filename}.wav", f"{filename}.mp3")

def convert_to_mp3(input_filename, output_filename):
    sound = AudioSegment.from_wav(input_filename)
    sound.export(output_filename, format="mp3")
    os.remove(input_filename)

if __name__ == "__main__":
    filename = "recorded_audio.wav"
    output_filename = "recorded_audio.mp3"
    duration = 10
    record_audio(filename, duration)
    # convert_to_mp3(filename, output_filename)
    print(f"Audio recorded and saved as {output_filename}")