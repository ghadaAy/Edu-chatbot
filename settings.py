from pydantic_settings import BaseSettings
from functools import lru_cache
import os



class Settings(BaseSettings):
    """
    Settings class for this application.
    Utilizes the BaseSettings from pydantic for environment variables.
    """
    
    temp_folder: str = "temp/"

    OPENAI_API_KEY: str 
    faiss_index_folder:str
    PATH_TESSERACT:str
    class Config:
        env_file = '.env'
        
@lru_cache(1)
def get_settings():
    """Function to get and cache settings.
    The settings are cached to avoid repeated disk I/O.
    """
    return Settings()

