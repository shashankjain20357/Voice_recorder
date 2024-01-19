import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play

def record_and_play(file_name, duration = 5, channels = 1, rate = 44100, chunk = 1024, format = pyaudio.paInt16):
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format = format,
                        channels = channels,
                        rate = rate,
                        input = True,
                        frames_per_buffer = chunk)

    print("Recording")
    frames = []
    for i in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording finished")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    audio_segment = AudioSegment.from_wav(file_name)
    print("Playing recorded audio")
    play(audio_segment)
    print("Playback finished")

if __name__ == "__main__":
    file_name = "recorded_audio.wav"
    record_duration = 10

    record_and_play(file_name, duration=record_duration)
    print(f"Audio recording saved as {file_name}")
