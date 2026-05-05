import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", encoding="utf-8-sig")

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


class NLPAssistantEngine:
    def __init__(self):
        self.current_dir = Path(__file__).resolve().parent
        self.base_models_dir = Path("E:/Uni/Models")
        self.minilm_local_path = str(self.base_models_dir / "all-MiniLM-L6-v2")
        self.data_dir = self.current_dir.parent / "volume"
        self.chroma_persist_dir = str(self.data_dir / "chroma_db")

        self.embedding_model = HuggingFaceEmbeddings(model_name=self.minilm_local_path)

        self.vectorstore = Chroma(
            persist_directory=self.chroma_persist_dir,
            embedding_function=self.embedding_model
        )

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to mkr/.env or the environment before starting the engine."
            )

        self.llm = ChatGroq(
            temperature=0.2,
            api_key=SecretStr(groq_api_key),
            model="llama-3.1-8b-instant"
        )

        system_prompt = (
            "Ти — розумний та корисний інформаційно-довідковий AI помічник для курсу 'Аналіз та обробка природної мови' (NLP). "
            "Використовуй наступний знайдений контекст для відповіді на запитання користувача. "
            "Якщо ти не знаєш відповіді або її немає в контексті, чесно скажи, що не знаєш, не вигадуй інформацію. "
            "Твоя відповідь буде озвучена синтезатором мовлення, тому уникай складного форматування (таблиць, довгого коду), "
            "роби речення лаконічними та природними.\n\n"
            "Контекст:\n{context}"
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)


    def generate_response(self, query: str) -> str:
        if not isinstance(query, str):
            query = str(query)
            
        response = self.rag_chain.invoke({"input": query})
        return response["answer"]

