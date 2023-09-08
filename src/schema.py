from pydantic import BaseModel

class RequestLLM(BaseModel):
    id_: str
    message: str 
class User(BaseModel):
    id_:str