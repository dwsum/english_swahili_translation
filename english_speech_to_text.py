import speech_recognition as sr
import whisper
from pathlib import Path
import os
import time
import glob
import numpy as np

# result = model.transcribe("audio.mp3")
# print(result["text"])


class english_speech_to_text:
    def __init__(self, model_name="english_speech_to_text_model"):
        self.model_name = model_name
        self.model = self.load_model()
        self.r = sr.Recognizer()

    def load_model(self):
        # return whisper.load_model("medium")
        # return whisper.load_model("base")
        return whisper.load_model("large")  # Load the Whisper model

    def transcribe(self, audio_file):
        # Placeholder for transcribing audio to text
        # return f"Transcription of {audio_file} using {self.model_name}."
        result = self.model.transcribe(audio_file, fp16=False) # Set fp16=False if not using a GPU
        # return result["text"]
        # text = self.r.recognize_whisper(audio_file, language="english")
        return result['text'].strip()

    def write_transcription(self, transcription, save_path, store_location="tmp/", log_location="log/"):
        with open(save_path, "w") as f:
            f.write(transcription)
        log_path = save_path.replace(store_location, log_location)
        with open(log_path, "w") as f:
            f.write(f"Transcription: {transcription}\n")

    def mic_to_audio_storage(self, duration_seconds=15):
        """
        Records audio for a set duration and saves it to a file.
        """
        store_location = "tmp/"
        Path(store_location).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        log_location = "log/"
        Path(log_location).mkdir(parents=True, exist_ok=True)

        # startup_message = "Hello and welcome to the Church of Jesus Christ of Latter-day Saints. "
        # startup_message += "This translation service may have occasional errors. " 
        # startup_message += "If there are any errors, please be patient and understanding. "
        # startup_message += "We are so glad you chose to come to church today."

        # self.write_transcription(startup_message, f"{store_location}startup_message.txt", store_location, log_location)
        while True:
            try:
                all_waveforms = list(glob.glob(f"{store_location}*.wav"))
                if len(all_waveforms) > 0:
                    # print(f"Found {len(all_waveforms)} audio files in {store_location}.")
                    all_waveforms = sorted(all_waveforms, key=os.path.getmtime)  # Sort by modification time
                    # print(f"Processing {len(all_waveforms)} audio files...")
                    if len(all_waveforms) == 1:
                        time.sleep(1) # wait to make sure it is not still being written to
                    # Process each audio file
                    for waveform in all_waveforms:
                        # print(f"Processing file: {waveform}")
                        transcription = self.transcribe(waveform)
                        # print(f"Transcription: {transcription}")
                        save_path = waveform.replace(".wav", "_transcription.txt").replace("recording_", "transcription_")
                        self.write_transcription(transcription, save_path, store_location, log_location)
                        # print(f"Transcription saved to: {save_path}")
                        # Optionally, remove the processed file
                        os.remove(waveform)
                else:
                    # print(f"No audio files found in {store_location}.")
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping recording.")
                break

if __name__ == "__main__":
    model = english_speech_to_text()
    # transcription = model.transcribe("New Recording 15.m4a")
    # transcription = model.transcribe("New Recording 15.m4a")
    # print(transcription)
    model.mic_to_audio_storage(duration_seconds=15)