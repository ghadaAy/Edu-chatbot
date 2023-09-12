import os
from queue import Queue
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from settings import get_settings
from src.llms.base import LanguageModelManager
from src import prompts as llms_prompts
from typing import Any, Optional, Awaitable, Callable, Union
import asyncio

app_settings = get_settings()


class OpenAIManager(LanguageModelManager):
    def __init__(self, prompt: str):
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
        )

    def load_openai_embeddings(self):
        return OpenAIEmbeddings(openai_api_key=app_settings.OPENAI_API_KEY)  # type: ignore

    def create_qa_prompt(self, prompt: str):
        return PromptTemplate(
            template=prompt,
            input_variables=["context", "question"],
        )
