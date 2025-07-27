import speech_recognition as sr
import librosa
import numpy as np
from moviepy.editor import VideoFileClip
import queue
import datetime
import sounddevice as sd
from scipy.io.wavfile import write  # Uncomment if you want to save the audio as
from pathlib import Path

# Constant for Whisper's expected sample rate
WHISPER_SAMPLE_RATE = 16000

# --- Configuration ---
SECONDS = 15  # Duration of each recording in seconds
SAMPLE_RATE = 44100  # Samples per second
CHANNELS = 1 # Mono audio

class audio_input:
    def __init__(self, duration_seconds=30):
        self.queue = queue.Queue()
        self.duration_seconds = duration_seconds

    def mic_to_audio_storage(self):
        """
        Records audio for a set duration and saves it to a file.
        """
        store_location="tmp/"
        Path(store_location).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        try:
            # print("Starting continuous recording... Press Ctrl+C to stop.")
            while True:
                # Generate a timestamp for the filename
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{store_location}recording_{timestamp}.wav"
                
                # print(f"🎙️  Recording for {SECONDS} seconds... Will save as '{filename}'")

                # print(f"\n🎙️  Listening for {SECONDS} seconds...")

                # Record audio directly into a NumPy array
                recording = sd.rec(int(SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
                sd.wait()  # Wait for the recording to complete

                # # The recording is already a NumPy array, but it needs to be a 1D float32 array
                # # .flatten() ensures it's 1D, which is what Whisper expects
                # audio_float32 = recording.flatten().astype(np.float32)

                # print("type of recording:", type(audio_float32))
                # print(f"✅ Finished recording. Length: {len(audio_float32)} samples")

                # self.queue.put(audio_float32)
                
                # Save the recording as a WAV file
                # The recording is scaled to 16-bit integer values
                write(filename, SAMPLE_RATE, (recording * 32767).astype(np.int16))
                
                # print(f"✅ Saved file: {filename}\n")
                
        except KeyboardInterrupt:
            # This block runs when the user presses Ctrl+C
            print("\nStopping recording.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def mic_to_audio(self):
        """
        Records audio for a set duration and saves it to a file.
        """
        try:
            print("Starting continuous recording... Press Ctrl+C to stop.")
            while True:
                # Generate a timestamp for the filename
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"recording_{timestamp}.wav"
                
                print(f"🎙️  Recording for {SECONDS} seconds... Will save as '{filename}'")

                print(f"\n🎙️  Listening for {SECONDS} seconds...")

                # Record audio directly into a NumPy array
                recording = sd.rec(int(SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
                sd.wait()  # Wait for the recording to complete

                # The recording is already a NumPy array, but it needs to be a 1D float32 array
                # .flatten() ensures it's 1D, which is what Whisper expects
                audio_float32 = recording.flatten().astype(np.float32)

                print("type of recording:", type(audio_float32))
                print(f"✅ Finished recording. Length: {len(audio_float32)} samples")

                self.queue.put(audio_float32)
                
                # Save the recording as a WAV file
                # The recording is scaled to 16-bit integer values
                # write(filename, SAMPLE_RATE, (recording * 32767).astype(np.int16))
                
                # print(f"✅ Saved file: {filename}\n")
                
        except KeyboardInterrupt:
            # This block runs when the user presses Ctrl+C
            print("\nStopping recording.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def mic_to_audio_old(self):
        # Create a Recognizer instance
        r = sr.Recognizer()

        print("Adjusting for ambient noise... Please wait.")
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            # Adjust the recognizer sensitivity to ambient noise
            # r.adjust_for_ambient_noise(source, duration=1)

            print("Say something! I'm listening...")
            while True:                
                # Listen for the first phrase and extract it into an AudioData object
                try:
                    audio = r.listen(source, timeout=15, phrase_time_limit=10)
                    self.queue.put(audio)
                except sr.WaitTimeoutError:
                    pass
                    

        print("Got it! Now transcribing...")

    def m4a_to_audio(self, file_path):
        # Load the audio file, sr=None preserves the original sample rate
        waveform, sample_rate = librosa.load(file_path, sr=None, mono=False)
        
        # If stereo, handle channels. We'll process the first channel [0] for simplicity.
        if waveform.ndim > 1:
            waveform = waveform[0]

        # Calculate chunk length in samples: 30 seconds * samples_per_second
        chunk_length_samples = 30 * sample_rate

        print(f"Audio loaded with sample rate: {sample_rate} Hz")
        print(f"Total samples: {len(waveform)}")

        # Split the waveform into 30-second chunks
        for i in range(0, len(waveform), chunk_length_samples):
            chunk = waveform[i:i + chunk_length_samples]
            # self.queue.append(chunk)
            self.queue.put(chunk)
            print(f"  Added chunk of {len(chunk)} samples to the queue.")

    def video_to_audio(self, video_path, duration_seconds=30):
        print(f"Loading video: {video_path}...")
        
        # try:
        # Use a with statement to ensure the file is closed automatically
        with VideoFileClip(video_path) as video_clip:
            if video_clip.audio is None:
                print("Error: The video file has no audio track.")
                return ""
            
            # Cut the clip to the desired duration
            if video_clip.duration < duration_seconds:
                print(f"Warning: Video is shorter than {duration_seconds} seconds. Processing full duration.")
                duration_seconds = video_clip.duration
            
            subclip = video_clip.subclip(0, duration_seconds)
            
            # Extract the audio and convert it to a NumPy array
            # Whisper expects a 32-bit float array at a 16kHz sample rate
            # audio_waveform = subclip.audio.to_soundarray(fps=WHISPER_SAMPLE_RATE)
            audio_waveform = subclip.audio.to_soundarray()

            # If the audio is stereo, convert it to mono by averaging the channels
            # if audio_waveform.ndim > 1 and audio_waveform.shape[1] == 2:
            #     audio_waveform = audio_waveform.mean(axis=1)

            # Transcribe the NumPy array
            self.queue.append(audio_waveform)
            return audio_waveform
        # except Exception as e:
        #     print(f"Error processing video file: {e}")
        #     return None
        
if __name__ == "__main__":
    audio_input_instance = audio_input(duration_seconds=15)
    # Uncomment to record from microphone
    audio_input_instance.mic_to_audio_storage()
    