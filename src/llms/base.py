import os
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferWindowMemory
from src.loader.process_file import ProcessFile
from settings import get_settings
import asyncio
from typing import Any, Optional, Awaitable, Callable, Union
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import Any, Optional, Awaitable, Callable, Union
import asyncio
import json
from src.callbacks.handler import ChainCallbackHandler

app_settings = get_settings()


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    try:
        await fn
    except Exception as e:
        # TODO: handle exception
        print(f"Caught exception: {e}")
    finally:
        # Signal the aiter to stop.
        event.set()


class LanguageModelManager:
    def __init__(
        self,
        language_model,
        embedding_function,
        qa_prompt,
        human_prefix,
        ai_prefix,
        data_path,
    ):
        self.language_model = language_model
        self.embedding_function = embedding_function
        self.qa_prompt = qa_prompt
        self.human_prefix = human_prefix
        self.ai_prefix = ai_prefix
        self.data_path = data_path
        self.conversation_chains = {}
        self.load_database()
        self.callback_handler = ChainCallbackHandler()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.language_model,
            chain_type="stuff",
            retriever=self.database.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.6, "k": 4},
            ),
            
            chain_type_kwargs={
                "prompt": self.qa_prompt,
                # "memory": ConversationBufferWindowMemory(
                #     human_prefix=self.human_prefix, ai_prefix=self.ai_prefix, k=4
                # ),
            },
            return_source_documents=False,
            verbose=True,
        )

    @classmethod
    def index_file_from_path(cls, file_path, embedding_function):
        try:
            documents = ProcessFile().process_document(file_path)
            if documents:
                cls.index_documents(documents, embedding_function)
        except Exception as e:
            raise ValueError(f"Error processing file: {e}")

    @classmethod
    def recursive_index_files(cls, mother_folder, embedding_function):
        print("Starting recursive file indexing...")
        list_documents = []
        for root, _, files in os.walk(mother_folder):
            for file in files:
                if not file.startswith("."):
                    file_path = os.path.join(root, file)
                    try:
                        documents = ProcessFile().process_document(file_path)
                        if documents:
                            list_documents.extend(documents)
                    except Exception as e:
                        print(f"Error processing file '{file}': {e}")

        if list_documents:
            cls.index_documents(list_documents, embedding_function)

        print("Indexing done!")

    @classmethod
    def index_documents(cls, documents, embedding_function):
        try:
            db = FAISS.load_local(app_settings.faiss_index_folder, embedding_function)
            new_faiss = db.from_documents(
                documents=documents, embedding=embedding_function
            )
            db.merge_from(new_faiss)
            db.save_local(folder_path=app_settings.faiss_index_folder)
        except:
            db = FAISS.from_documents(documents=documents, embedding=embedding_function)
            db.save_local(folder_path=app_settings.faiss_index_folder)

    async def run_qa_chain(self, query: str, user_id: str):
        self.callback_handler.on_llm_end()
        if self.database is None:
            self.load_database()
        self.qa_chain.run(query, callbacks=[self.callback_handler])

        for token in self.callback_handler.tokens:
            yield json.dumps({"user_id": user_id, "token": token})
        
        # for token in self.qa_chain.run(query):
        #     yield json.dumps({"user_id": user_id, "token": token})

    def load_database(self):
        from langchain.vectorstores import FAISS

        faiss_index_folder = app_settings.faiss_index_folder
        try:
            self.database = FAISS.load_local(
                faiss_index_folder, self.embedding_function
            )
        except ValueError:
            print(
                f"There is no database under the name {faiss_index_folder}, index some documents first"
            )
