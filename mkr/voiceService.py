import os
import edge_tts

from dotenv import load_dotenv
load_dotenv()

from groq import AsyncGroq

class VoiceService:
    def __init__(self):
        self.audio_output_dir = "./volume/audio"
        os.makedirs(self.audio_output_dir, exist_ok=True)

        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.voice = "uk-UA-PolinaNeural"

        self.whisper_model = "whisper-large-v3"

    async def text_to_speech(self, text: str, filename: str = "response.mp3") -> str:
        output_path = os.path.join(self.audio_output_dir, filename)
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        return output_path

    nlp_domain_prompt = (
        "NLP, Natural Language Processing, LLM, токенізація, лематизація, "
        "стемінг, ембеддінги, трансформери, векторизація, векторні бази даних, "
        "ChromaDB, RAG, Hugging Face, GeeksforGeeks, NLTK, spaCy, парсинг"
    )

    async def speech_to_text(self, audio_file_path: str) -> str:
        with open(audio_file_path, "rb") as file:
            transcription = await self.groq_client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model=self.whisper_model,
                language="uk",
                prompt=self.nlp_domain_prompt,
            )

        return transcription.text


