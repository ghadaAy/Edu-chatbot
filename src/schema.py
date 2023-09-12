from pydantic import BaseModel

class RequestLLM(BaseModel):
    user_id: str
    message: str 
