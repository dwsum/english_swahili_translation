import glob
from pathlib import Path

def evaluate(log_path):

    all_transcription_logs = list(glob.glob(f"{log_path}/transcription*.txt"))

    # sort logs by modification time
    all_transcription_logs.sort()

    for log_file in all_transcription_logs:

        with open(log_file, "r") as f:
            transcription = f.read().strip()
        print(f"Transcription from audio in: {transcription}")
        translated_file = log_file.replace("transcription", "translated").replace(".txt", "_translated.txt")
        
        if not Path(translated_file).exists():
            raise FileNotFoundError(f"Translated file not found: {translated_file}")
        
        with open(translated_file, "r") as f:
            translated_text = f.read().strip()
        print(f"Translated Text: {translated_text}")

        print("Translated back to English with Google Translate:")
        print("")


if __name__ == "__main__":
    log_path = "log/"
    evaluate(log_path)
