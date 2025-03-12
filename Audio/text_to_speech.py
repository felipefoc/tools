from TTS.api import TTS
import torch
from pydub import AudioSegment
import os

class TtsConfig:
    def __init__(self):
        self.model = "tts_models/multilingual/multi-dataset/xtts_v2"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.speaker = "Gilberto Mathias" # "Alma María"
        self.compute_type = "float16"

    def to_tts_model(self) -> TTS:
        return TTS(self.model).to(self.device)

    def list_avaiable_models(self) -> list:
        return self.to_tts_model().list_models()

    def list_avaiable_speakers(self):
        return self.to_tts_model().speakers

    def simple_tts_to_file(self, text: str, file_path: str, language="pt", speed=1.2, from_audio_sample=None):
        print(f"Starting TTS... Device: {self.device}")
        if from_audio_sample:
            self.to_tts_model().tts_to_file(
                text=text,
                file_path=file_path,
                language=language,
                speed=speed,
                speaker_wav=from_audio_sample
            )
        else:
            self.to_tts_model().tts_to_file(
                text=text, 
                file_path=file_path, 
                speaker=self.speaker, 
                language=language,
                speed=speed
            )
        return file_path

ttsConfig = TtsConfig() 
text = """
Lorem Ipsum
"""

def separate_text_into_sentences(text: str) -> list:
    # Split text into sentences using multiple delimiters
    sentences = []
    for delimiter in [".", "\n", "!", "?"]:
        if not sentences:
            sentences = text.split(delimiter)
        else:
            temp = []
            for sentence in sentences:
                temp.extend(sentence.split(delimiter))
            sentences = temp
    
    # Filter and clean sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Combine sentences that are too short and split ones that are too long
    max_chars = 230  # Conservative limit to stay under 400 tokens
    processed_sentences = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk = (current_chunk + " " + sentence).strip()
        else:
            if current_chunk:
                processed_sentences.append(current_chunk)
            current_chunk = sentence
    
    if current_chunk:  # Add the last chunk
        processed_sentences.append(current_chunk)
    
    return processed_sentences

def remove_temp_audio_files(audio_files: list):
    for audio in audios:
        os.remove(audio)

# Generate individual audio files
def generate_individual_audio_files(text: str):
    sentences = separate_text_into_sentences(text)
    audio_files = []
    for i, chunk in enumerate(sentences):
        output_file = f"output{i}.wav"
        ttsConfig.simple_tts_to_file(
            from_audio_sample="Audio/sample.wav",
            text=chunk,
            file_path=output_file
        )
        audio_files.append(output_file)
    return audio_files

# Merge all audio files
def merge_audio_files(audio_files: list):
    combined_audio = AudioSegment.empty()
    for audio_file in audio_files:
        sound = AudioSegment.from_wav(audio_file)
        combined_audio += sound
    combined_audio.export("final_output.wav", format="wav")
    remove_temp_audio_files(audio_files)
    return "final_output.wav"

# audios = generate_individual_audio_files(text)
# merge_audio_files(audios)

