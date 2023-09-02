import os
from langchain.vectorstores import FAISS
from src.llms.base import LLM


class FAISS_changed(FAISS):
    @classmethod
    def from_documents(cls, documents, embeddings, fais_index:str="default_faiss_index"):
        faiss_db= cls.from_documents(documents, embeddings)
        try:
            local_index=FAISS.load_local(fais_index, embeddings)
            local_index.merge_from(faiss_db)
            local_index.save_local(fais_index)
        except FileNotFoundError:
            faiss_db.save_local(folder_path=fais_index)
        return faiss_db