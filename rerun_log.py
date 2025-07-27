import glob
from pathlib import Path

from english_to_swahili_translation import english_to_swahili_translation

def rerun_translation(path_to_log, save_path="tmp_rerun_log/"):

    all_logs = list(glob.glob(f"{path_to_log}/transcription*.txt"))

    all_logs.sort()  # Sort logs by modification time

    translator = english_to_swahili_translation()

    for log_file in all_logs:
        with open(log_file, "r") as f:
            transcription = f.read().strip()
        # remove the first transcription line
        if transcription.startswith("Transcription: "):
            transcription = transcription.replace("Transcription: ", "", 1)

        print("Transcription from audio in: ", transcription)

        translated_text = translator.translate_english_to_swahili(transcription)
        print(f"Translated Text: {translated_text}")

        print("Translated back to English with Google Translate:")
        print("")

if __name__ == "__main__":
    log_path = "log/"
    rerun_translation(log_path, save_path="tmp_rerun_log/")