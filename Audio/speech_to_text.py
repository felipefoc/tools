from faster_whisper import WhisperModel
import speech_recognition as sr
import torch
import tempfile

class SttConfig:
    def __init__(self):
        self.model_size = "turbo"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16"

    @property
    def gpu_avaiable(self):
        return torch.cuda.is_available() == True

    def to_whisper_modal(self):
        return WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)

    def listen(self, simple_transcribe=False):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait...")
            r.adjust_for_ambient_noise(source)
            print("Speak something...")
            r.pause_threshold = 2 # Wait for 1 seconds of silence before stopping
            r.energy_threshold = 300  # Minimum audio energy to consider as speech
            audio_data = r.listen(source)
            ### Using speech_recognition with faster_whisper
            if simple_transcribe:
                return r.recognize_faster_whisper(
                    audio_data,
                    model=self.model_size, 
                    init_options={
                        "device": self.device,
                        "compute_type": self.compute_type 
                    },
                    beam_size=5
                )

        return audio_data

    ### Using faster_whisper model 
    def transcribe(self, audio) -> str:
        print("Starting transcription...")
        transcribe_text = ""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            temp_audio_file.write(audio.get_wav_data())
            temp_filename = temp_audio_file.name
            model = self.to_whisper_modal()
            segments, info = model.transcribe(temp_filename, beam_size=5)
            print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
            for segment in segments:
                transcribe_text += segment.text + " "
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            temp_audio_file.flush()

        return transcribe_text

### Example of use with speech_recognition:
# stt = SttConfig()
# audio_data = stt.listen(simple_transcribe=True)
# print(audio_data)

### Example of use with faster_whisper:
# stt = SttConfig()
# audio_data = stt.listen()
# text = stt.transcribe(audio_data)