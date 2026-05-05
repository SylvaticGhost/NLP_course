import json
import os
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_MODELS_DIR = "E:/Uni/Models"
minilm_name = "all-MiniLM-L6-v2"
MINILM_LOCAL_PATH = os.path.join(BASE_MODELS_DIR, minilm_name)

DATA_DIR = "./../volume"
CHROMA_PERSIST_DIR = os.path.join(DATA_DIR, "chroma_db")

with open(f"{DATA_DIR}/nlp_reference_materials.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

documents_for_chroma = []
for item in loaded_data:
    doc = Document(
        page_content=item["page_content"],
        metadata=item["metadata"]
    )
    documents_for_chroma.append(doc)

print(f"Відновлено {len(documents_for_chroma)} чанків (документів).")

print("2. Ініціалізація локальної моделі ембеддінгів...")
embedding_model = HuggingFaceEmbeddings(model_name=MINILM_LOCAL_PATH)

print("3. Векторизація тексту та збереження у ChromaDB...")
vectorstore = Chroma.from_documents(
    documents=documents_for_chroma,
    embedding=embedding_model,
    persist_directory=CHROMA_PERSIST_DIR
)

print(f"\nГотово! Векторну базу успішно збережено у директорію: {CHROMA_PERSIST_DIR}")