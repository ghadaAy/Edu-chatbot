import os
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from settings import get_settings
from src.llms.base import LanguageModelManager
from src import prompts as llms_prompts
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import Any, Optional, Awaitable, Callable, Union
import asyncio

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

class OpenAIManager(LanguageModelManager):
    def __init__(self, prompt:str):
        self.callback=AsyncIteratorCallbackHandler()
        super().__init__(
            
            language_model=self.load_openai_language_model(),
            embedding_function=self.load_openai_embeddings(),
            qa_prompt=self.create_qa_prompt(prompt),
            human_prefix="Human",
            ai_prefix="AI",
            data_path="./data",
            
        )
        
        

    def load_openai_language_model(self):
        
        return ChatOpenAI(
            openai_api_key=app_settings.OPENAI_API_KEY,
            temperature=0,
            verbose=True,
            max_tokens=1024,
            streaming=True,
            callbacks=[self.callback]
        )

    def load_openai_embeddings(self):
        return OpenAIEmbeddings(openai_api_key=app_settings.OPENAI_API_KEY)  # type: ignore

    def create_qa_prompt(self, prompt:str):
        return PromptTemplate(
            template=prompt,
            input_variables=["context", "question"],
        )
    async def answer(self, msg):
     # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(self.run_qa_chain(msg), self.callback.done))

        async for token in self.callback.aiter():
            # Use server-sent-events to stream the response
            yield token

        await task