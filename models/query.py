from typing import List
from pydantic import BaseModel, field_validator
from fastapi import FastAPI, UploadFile, HTTPException, Query,Depends
from src.app.src import llms
from pydantic import BaseModel
import uvicorn

app = FastAPI()
openai_llm_dict = {"AzureGPT35Turbo16k": llms.AzureGPT35Turbo16k()}
llama_llm_dict = {
    # "Llama2": llms.Llama2()
}
llm_dict = {}
llm_dict.update(llama_llm_dict)
llm_dict.update(openai_llm_dict)


llm_names = list(llm_dict.keys())
default_llm = llm_names[0]
class QueryBase(BaseModel):
    msg: str
    BrainIds:list[str]
    conversation_id: str = "NONE",
    mode: str 
    llm_name: str 

@field_validator('BrainIds')
@classmethod
def str_to_int(cls, v: str, info):
    context = info.context
    if context:
        brain_ids = context.get('BrainIds', set())
        try:
            brain_ids = [int(id_) for id_ in brain_ids]
        except:
            raise TypeError("brainIds should be a list of strings that can be turned into integeres")
    return brain_ids
@app.get("/")
def read_root(student: QueryBase = Depends()):
    return {"brainids": student.BrainIds}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)