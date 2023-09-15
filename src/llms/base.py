import os
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from src.loader.process_file import ProcessFile
from settings import get_settings
import asyncio
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from src.callbacks.handler import EnqueueCallbackHandler

app_settings = get_settings()
class LanguageModelManager:
    def __init__(
        self,
        language_model,
        embedding_function,
        human_prefix,
        ai_prefix,
        data_path,
        prompt_template,
    ):
        self.language_model = language_model
        self.embedding_function = embedding_function
        self.human_prefix = human_prefix
        self.ai_prefix = ai_prefix
        self.data_path = data_path
        self.load_database()
        self.memory = ConversationBufferMemory(memory_key="chat_history")

        self.prompt_template = prompt_template
        self.queues = {}
        

        

    def create_qa_prompt(self, prompt_template: str):
        return PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"],
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

    async def run_qa_chain(self, query: str, message_id:str):
        if message_id not in self.queues:
            self.queues[message_id] = asyncio.Queue()
        self.callback_handler = EnqueueCallbackHandler(self.queues, message_id=message_id)

        docs_and_scores = self.database.similarity_search_with_score(query)
        str_docs = "\n".join([doc[0].page_content for doc in docs_and_scores])

        qa_prompt = self.create_qa_prompt(prompt_template=self.prompt_template)
        chain = LLMChain(
            llm=self.language_model,
            callbacks=[self.callback_handler],
            prompt=qa_prompt,
            # =memory=self.memory,
            verbose=True,
        )

        await chain.arun(
            callbacks=[self.callback_handler], context=str_docs, question=query
        )

        while True:
            response = await self.queues[message_id].get()
            if response is None:
                break
            yield response
            
            self.queues[message_id].task_done()

       
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
