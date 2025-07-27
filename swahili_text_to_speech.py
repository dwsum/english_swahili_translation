import torch
import numpy as np
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer
import sounddevice as sd
import glob
import time
from pathlib import Path
import os

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


        # Write to WAV file
        # scipy.io.wavfile.write("out.wav", rate=self.model.config.sampling_rate, data=output_np)
    
    def generate_speech_from_file(self):
        save_path = "tmp/"

        while True:
            try:
                all_files = list(glob.glob(f"{save_path}translated_*.txt"))
                if len(all_files) > 0:
                    all_files = sorted(all_files, key=os.path.getmtime)  # Sort by modification time
                    if len(all_files) == 1:
                        time.sleep(1)  # wait to make sure it is not still being written to
                    # Process each text file
                    for file_path in all_files:
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

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model_name = "Benjamin-png/swahili-mms-tts-finetuned"
# text = "Habari, karibu kwenye mfumo wetu wa kusikiliza kwa Kiswahili."
# audio_file_path = "swahili_speech.wav"

# # Load model and tokenizer dynamically based on the provided model name
# model = VitsModel.from_pretrained(model_name).to(device)
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# # Step 1: Tokenize the input text
# inputs = tokenizer(text, return_tensors="pt").to(device)

# # Step 2: Generate waveform
# with torch.no_grad():
#     output = model(**inputs).waveform

# # Step 3: Convert PyTorch tensor to NumPy array
# output_np = output.squeeze().cpu().numpy()

# # Step 4: Write to WAV file
# scipy.io.wavfile.write(audio_file_path, rate=model.config.sampling_rate, data=output_np)
# play(output_np, model.config.sampling_rate)