import torch
import numpy as np
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer
import sounddevice as sd
import glob
import time
from pathlib import Path
import os

from constants import *

class swahili_text_to_speech:
    def __init__(self, model_name="swahili_text_to_speech_model"):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_name = "Benjamin-png/swahili-mms-tts-finetuned"
        self.model = VitsModel.from_pretrained(model_name).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_speech(self, text):
        # Tokenize the input text
        inputs = self.tokenizer(text, return_tensors="pt")
        
        # Generate waveform
        with torch.no_grad():
            output = self.model(**inputs).waveform
        
        # Convert PyTorch tensor to NumPy array
        output_np = output.squeeze().cpu().numpy()
        
        sd.play(output_np, self.model.config.sampling_rate)
        sd.wait()  # Wait until the sound has finished playing
    
    def generate_speech_from_file(self):
        Path(RUNNING_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

        while True:
            if not Path(RUNNING_DIR).exists():
                break
            try:
                all_files = list(glob.glob(f"{TMP_DIR}translated_*.txt"))
                if len(all_files) > 0:
                    all_files = sorted(all_files, key=os.path.getmtime)  # Sort by modification time
                    if len(all_files) == 1:
                        time.sleep(1)  # wait to make sure it is not still being written to
                    # Process each text file
                    for file_path in all_files:
                        if not Path(RUNNING_DIR).exists():
                            break
                        with open(file_path, "r") as f:
                            text = f.read().strip()
                        self.generate_speech(text)
                        # Optionally, remove the processed file
                        os.remove(file_path)
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping speech generation.")
                break

if __name__ == "__main__":
    tts_model = swahili_text_to_speech()
    # Example usage
    tts_model.generate_speech_from_file()
