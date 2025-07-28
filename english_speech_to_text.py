import speech_recognition as sr
import whisper
from pathlib import Path
import os
import time
import glob
import numpy as np
from constants import *
import datetime


class english_speech_to_text:
    def __init__(self, model_name="english_speech_to_text_model"):
        self.model_name = model_name
        self.model = self.load_model()
        self.r = sr.Recognizer()

    def load_model(self):
        return whisper.load_model("large")  # Load the Whisper model

    def transcribe(self, audio_file):
        result = self.model.transcribe(audio_file, fp16=False) # Set fp16=False if not using a GPU
        return result['text'].strip()

    def write_transcription(self, transcription, save_path):
        with open(save_path, "w") as f:
            f.write(transcription)
        log_path = save_path.replace(TMP_DIR, LOG_DIR)
        with open(log_path, "w") as f:
            f.write(f"Transcription: {transcription}\n")

    def mic_to_audio_storage(self):
        """
        Records audio for a set duration and saves it to a file.
        """
        Path(TMP_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        Path(RUNNING_DIR).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now()
        # Make timestamp at 1am.
        timestamp = timestamp.replace(hour=1, minute=0, second=0, microsecond=0)
        timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{TMP_DIR}/transcription_{timestamp}_transcription.txt"

        self.write_transcription(STARTUP_MESSAGE, filename)

        while True:
            try:

                all_waveforms = list(glob.glob(f"{TMP_DIR}*.wav"))
                if len(all_waveforms) > 0:
                    all_waveforms = sorted(all_waveforms, key=os.path.getmtime)  # Sort by modification time
                    if len(all_waveforms) == 1:
                        time.sleep(1) # wait to make sure it is not still being written to
                    # Process each audio file
                    for waveform in all_waveforms:
                        if not Path(RUNNING_DIR).exists():
                            break
                        transcription = self.transcribe(waveform)
                        save_path = waveform.replace(".wav", "_transcription.txt").replace("recording_", "transcription_")
                        self.write_transcription(transcription, save_path)
                        os.remove(waveform)
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                break
            if not Path(RUNNING_DIR).exists():
                break

if __name__ == "__main__":
    model = english_speech_to_text()
    model.mic_to_audio_storage()