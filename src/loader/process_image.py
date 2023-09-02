import logging
from settings import get_settings
from typing import List, Union
from src.loader.base import BaseProcessor
from langchain.document_loaders.image import UnstructuredImageLoader
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

app_settings = get_settings()
pytesseract.pytesseract.tesseract_cmd = app_settings.PATH_TESSERACT  # your path may be different


class ProcessImage(BaseProcessor):
    
    def load_single_image(self, source: str) -> Union[Document, None]:
        
        loader = UnstructuredImageLoader(source)
        data = loader.load()
        return data

    def process_document(self, source: str) -> Union[List[Document], None]:
        """Loads a document and recursively splits it to create docs.

        Args:
            source (str): Path to the file.

        Returns:
            list of Documents or None
        """
        logging.info(f"Processing file {source}")
        docs = self.load_single_image(source)
        if docs is not None:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            try:
                docs = text_splitter.split_documents(docs) # type: ignore
                logging.info("Processing successful")
                return docs
            except Exception as e:
                logging.error(f"Error splitting document: {e}")
                return None
