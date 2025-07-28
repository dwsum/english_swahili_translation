from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import time
from pathlib import Path
import glob
import queue

import sentencepiece as spm
from ctranslate2 import Translator

from constants import *

class english_to_swahili_translation:
    def __init__(self):
        path_to_model = "/Users/drewsumsion/Downloads/model_files"
        source = 'en'
        target = 'sw'

        self.translator = Translator(path_to_model, compute_type='int8')
        self.source_tokenizer = spm.SentencePieceProcessor(f'{path_to_model}/{source}.spm.model')
        self.target_tokenizer = spm.SentencePieceProcessor(f'{path_to_model}/{target}.spm.model')

    def translate_english_to_swahili(self, text):
        text = [text]

        input_tokens = self.source_tokenizer.EncodeAsPieces(text)
        translator_output = self.translator.translate_batch(
          input_tokens,
          batch_type='tokens',
          beam_size=2,
          max_input_length=0,
          max_decoding_length=256
        )

        output_tokens = [item.hypotheses[0] for item in translator_output]
        translation = self.target_tokenizer.DecodePieces(output_tokens)

        return translation[0]

    def translate_english_to_swahili_from_file(self):

        Path(TMP_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the
        Path(RUNNING_DIR).mkdir(parents=True, exist_ok=True)
        while True:
            if not Path(RUNNING_DIR).exists():
                break
            try:
                all_files = list(glob.glob(f"{TMP_DIR}transcription_*.txt"))
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

                        translated_text = self.translate_english_to_swahili(text)
                        
                        save_translated_path = file_path.replace(".txt", "_translated.txt").replace("transcription_", "translated_")
                        # Save the translated text to a new file
                        with open(save_translated_path, "w") as f:
                            f.write(translated_text)
                        save_log_path = save_translated_path.replace(TMP_DIR, LOG_DIR)
                        with open(save_log_path, "w") as f:
                            f.write(translated_text)
                        # Remove the original file
                        os.remove(file_path)
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                # This block runs when the user presses Ctrl+C
                print("\nStopping translation.")
                break

if __name__ == "__main__":
    translator = english_to_swahili_translation()
    # text = "Hello, how are you?"
    # translated_text = translator.translate_english_to_swahili(text)
    # print(translated_text)
    translator.translate_english_to_swahili_from_file()