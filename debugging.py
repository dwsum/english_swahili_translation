import sounddevice as sd
import numpy as np
import whisper

# --- Configuration ---
SECONDS = 10  # Duration of each recording
SAMPLE_RATE = 16000  # Whisper works best with 16kHz
CHANNELS = 1 # Mono audio

def listen_and_transcribe():
    """
    Continuously listens for audio, transcribes it in memory, and prints the result.
    """
    print("Loading Whisper model...")
    # Load the model once at the beginning
    model = whisper.load_model("base")
    print("Model loaded. Starting real-time transcription. Press Ctrl+C to stop.")

    try:
        while True:
            print(f"\n🎙️  Listening for {SECONDS} seconds...")

            # Record audio directly into a NumPy array
            recording = sd.rec(int(SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
            sd.wait()  # Wait for the recording to complete

            print("Transcribing audio...")

            # The recording is already a NumPy array, but it needs to be a 1D float32 array
            # .flatten() ensures it's 1D, which is what Whisper expects
            audio_float32 = recording.flatten().astype(np.float32)

            # Transcribe the NumPy array directly
            result = model.transcribe(audio_float32, fp16=False) # Set fp16=False if not using a GPU

            # Print the transcribed text
            print(">>>", result['text'].strip())

    except KeyboardInterrupt:
        print("\nStopping transcription.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function
if __name__ == "__main__":
    listen_and_transcribe()