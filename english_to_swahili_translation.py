from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import time
from pathlib import Path
import glob
import queue

import sentencepiece as spm
from ctranslate2 import Translator

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


    
    # def __init__(self):
    #     model_checkpoint = "Rogendo/en-sw"
    #     self.fine_tuned_model = pipeline("translation", model=model_checkpoint)

    # def translate_english_to_swahili(self, text):
    #     # translated_text = self.eng_swa_translator(text, max_length=128, num_beams=5)[0]['generated_text']
    #     # return translated_text
    #     return self.fine_tuned_model(text)[0]['translation_text']

    def translate_english_to_swahili_from_file(self):
        save_path = "tmp/"
        log_path = "log/"
        Path(save_path).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        Path(log_path).mkdir(parents=True, exist_ok=True)  # Ensure the
        while True:
            try:
                all_files = list(glob.glob(f"{save_path}transcription_*.txt"))
                if len(all_files) > 0:
                    # print(f"Found {len(all_files)} text files in {save_path}.")
                    all_files = sorted(all_files, key=os.path.getmtime)  # Sort by modification time
                    # print(f"Processing {len(all_files)} text files...")
                    if len(all_files) == 1:
                        time.sleep(1)  # wait to make sure it is not still being written to
                    # Process each text file
                    for file_path in all_files:
                        # print(f"Processing file: {file_path}")
                        with open(file_path, "r") as f:
                            text = f.read().strip()

                        translated_text = self.translate_english_to_swahili(text)
                        # print(f"Translated Text: {translated_text}")
                        save_translated_path = file_path.replace(".txt", "_translated.txt").replace("transcription_", "translated_")
                        # Save the translated text to a new file
                        with open(save_translated_path, "w") as f:
                            f.write(translated_text)
                        save_log_path = save_translated_path.replace(save_path, log_path)
                        with open(save_log_path, "w") as f:
                            f.write(translated_text)
                        # print(f"Translated text saved to: {save_translated_path}")
                        # Optionally, remove the processed file
                        os.remove(file_path)
                else:
                    # print(f"No text files found in {save_path}.")
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