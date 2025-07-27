from english_speech_to_text import english_speech_to_text
from english_to_swahili_translation import english_to_swahili_translation
from swahili_text_to_speech import swahili_text_to_speech
from audio_input import audio_input
import time
import threading
import queue

class run_all:
    def __init__(self, duration_seconds=30):
        self.translator = english_to_swahili_translation()
        self.speech_to_text_model = english_speech_to_text()
        self.text_to_speech_model = swahili_text_to_speech()
        # self.audio_input_model = audio_input()

        self.transcriptions = queue.Queue()
        self.translated_texts = queue.Queue()

        # self.lock = threading.Lock()
        # self.condition = threading.Condition(self.lock)

        # self.record_audio_thread = threading.Thread(target=self.audio_input_model.mic_to_audio)
        self.speech_to_text_thread = threading.Thread(target=self.thread_run_speech_to_text)
        self.translation_thread = threading.Thread(target=self.thread_english_to_swahili_translation)
        self.text_to_speech_thread = threading.Thread(target=self.thread_swahili_text_to_speech)

    def thread_run_speech_to_text(self):
        while True:
            audio_waveform = self.audio_input_model.queue.get()
            print(f"Received audio waveform of length: {len(audio_waveform)}")
            start_time = time.time()
            transcription = self.speech_to_text_model.transcribe(audio_waveform)
            print("Transcription:", transcription)
            self.transcriptions.put(transcription)
            end_time = time.time()
            print(f"Transcription: {transcription}")
            print(f"Length of transcription: {len(transcription)} characters")
            print(f"Time taken for transcription: {end_time - start_time} seconds")
    
    def thread_english_to_swahili_translation(self):
        while True:
            if not self.transcriptions.empty():
                transcription = self.transcriptions.get()
                start_time = time.time()
                translated_text = self.translator.translate_english_to_swahili(transcription)
                if len(translated_text) > 0:
                    print(f"Translated Text: {translated_text}")
                self.translated_texts.put(translated_text)
                end_time = time.time()
                print(f"Translated Text: {translated_text}")
                print(f"Time taken for translation: {end_time - start_time} seconds")

    def thread_swahili_text_to_speech(self):
        while True:
            if not self.translated_texts.empty():
                translated_text = self.translated_texts.get()
                start_time = time.time()
                self.text_to_speech_model.generate_speech(translated_text)
                end_time = time.time()
                print(f"Generated speech for: {translated_text}")
                print(f"Time taken for speech generation: {end_time - start_time} seconds")

    def run_all(self):
        # Start the speech-to-text thread
        self.record_audio_thread.start()
        self.speech_to_text_thread.start()
        self.translation_thread.start()
        self.text_to_speech_thread.start()

        self.record_audio_thread.join()
        self.speech_to_text_thread.join()
        self.translation_thread.join()
        self.text_to_speech_thread.join()

    def run_all_audio_file(self, audio_file):
        # Step 1: Transcribe English speech to text
        transcription = self.speech_to_text_model.transcribe(audio_file)
        print(f"Transcription: {transcription}")
        # Step 2: Translate English text to Swahili
        translated_text = self.translator.translate_english_to_swahili(transcription)
        print(f"Translated Text: {translated_text}")
        # Step 3: Convert Swahili text to speech
        self.text_to_speech_model.generate_speech(translated_text)
        print(f"Generated speech for: {translated_text}")

if __name__ == "__main__":
    runner = run_all(duration_seconds=15)
    
    # transcription = model.transcribe("New Recording 15.m4a")
    # print(transcription)
    # my_audio_input = audio_input()
    # video_path = "zjkassk10avoapm9idh2wyqbmqk4615m3i11a1i3-360p-en.mp4"  # Replace with your video
    # audio_waveform = my_audio_input.video_to_audio(video_path)
    # runner.audio_input_model.m4a_to_audio("New Recording 16 copy.m4a")
    # print(type(audio_waveform))
    # start_time = time.time()
    # # runner.run_all_audio_file("New Recording 15.m4a")
    # runner.run_all_audio_file("New Recording 16 copy.m4a")
    # end_time = time.time()
    # print(f"Total time taken: {end_time - start_time} seconds")

    runner.run_all()