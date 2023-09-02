from settings import get_settings
from abc import ABC, abstractmethod
app_settings= get_settings()

class BaseProcessor(ABC):
    """
    Abstract base class for indexing Frequently Asked Questions (FAQ) documents.

    Subclasses of `BaseProcessor` must implement the abstract methods defined here
    to provide specific implementations for loading, processing, and adding metadata
    to FAQ documents.

    Attributes:
        None

    Methods:
        load_single_document(source: str):
            Load a single FAQ document from the specified source.
        
        process_document(source: str):
            Process the content of a FAQ document from the specified source.
        
        add_metadata_to_document(docs: List[Document], metadata: dict = {}):
            Add metadata to a list of FAQ documents.

    Usage Example:
    ```python
    class MyBaseProcessor(BaseProcessor):
        def load_single_document(source: str):
            # Implementation specific to loading a FAQ document.
        
        def process_document(source: str):
            # Implementation specific to processing a FAQ document.
        
        def add_metadata_to_document(docs: List[Document], metadata: dict = {}):
            # Implementation specific to adding metadata to FAQ documents.
    ```
    """

    
    @abstractmethod    
    def process_document(source: str):
        pass
    
