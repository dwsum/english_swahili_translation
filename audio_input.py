import speech_recognition as sr
import librosa
import numpy as np
from moviepy.editor import VideoFileClip
import queue
import datetime
import sounddevice as sd
from scipy.io.wavfile import write  # Uncomment if you want to save the audio as
from pathlib import Path
from constants import *

# Constant for Whisper's expected sample rate
WHISPER_SAMPLE_RATE = 16000

# --- Configuration ---
SAMPLE_RATE = 44100  # Samples per second
CHANNELS = 1 # Mono audio

class audio_input:
    def __init__(self):
        self.queue = queue.Queue()

    def mic_to_audio_storage(self):
        """
        Records audio for a set duration and saves it to a file.
        """
        Path(TMP_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        Path(RUNNING_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        try:
            # print("Starting continuous recording... Press Ctrl+C to stop.")
            while True:
                # Generate a timestamp for the filename
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{TMP_DIR}recording_{timestamp}.wav"

                # Record audio directly into a NumPy array
                recording = sd.rec(int(RUN_TIME * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
                sd.wait()  # Wait for the recording to complete

                write(filename, SAMPLE_RATE, (recording * 32767).astype(np.int16))

                if not Path(RUNNING_DIR).exists():
                    break                    
                
        except KeyboardInterrupt:
            # This block runs when the user presses Ctrl+C
            print("\nStopping recording.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def mp3_to_audio_storage(self, audio_file):
        """
        Converts an MP3 file to WAV format and saves it to the temporary directory.
        """
        Path(TMP_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        
        # Load the audio file using librosa
        audio, sr = librosa.load(audio_file, sr=WHISPER_SAMPLE_RATE)

        # split the audio into chunks if it's longer than RUN_TIME
        if len(audio) > RUN_TIME * WHISPER_SAMPLE_RATE:
            num_chunks = int(np.ceil(len(audio) / (RUN_TIME * WHISPER_SAMPLE_RATE)))
            for i in range(num_chunks):
                start = i * RUN_TIME * WHISPER_SAMPLE_RATE
                end = min((i + 1) * RUN_TIME * WHISPER_SAMPLE_RATE, len(audio))
                chunk = audio[start:end]

                # Generate a timestamp for the filename
                timestamp = datetime.datetime.now()
                # add i seconds to the timestamp
                timestamp += datetime.timedelta(seconds=i)
                timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{TMP_DIR}recording_{timestamp}.wav"

                # Save the chunk as a WAV file
                write(filename, WHISPER_SAMPLE_RATE, (chunk * 32767).astype(np.int16))


if __name__ == "__main__":
    audio_input_instance = audio_input()
    # Uncomment to record from microphone
    audio_input_instance.mic_to_audio_storage()

    # audio_file = "v4s5aqokcv8ap0q8cva0qdtvtpdiz5awrtlo7kiq-128k-en.mp3"
    # audio_input_instance.mp3_to_audio_storage(audio_file)
    