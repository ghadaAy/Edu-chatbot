from pydantic import BaseModel

class RequestLLM(BaseModel):
    message_id: str
    message: str 
