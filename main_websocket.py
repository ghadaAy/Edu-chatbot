from venv import logger
from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from src.prompts import summarize_prompt, openai_prompt_template
from settings import get_settings
from src.llms.openai import OpenAIManager
from src.prompts import summarize_prompt, openai_prompt_template
import uvicorn
app_settings = get_settings()
app = FastAPI()


openai_summarizing = OpenAIManager(prompt=summarize_prompt)
openai_qa = OpenAIManager(prompt=openai_prompt_template)


app = FastAPI()
websocket_clients = []

@app.websocket("/summarizing")
async def ask_for_summarization(websocket:WebSocket, user_id:str=Query(...)):
    
    try:
        await websocket.accept()
        websocket_clients.append(websocket)
        while True:
            
            message = await websocket.receive_text()
            async for token in openai_summarizing.run_qa_chain(message, user_id):
                await websocket.send_text(token)
    except WebSocketDisconnect:
        logger.info("websocket out")
        # websocket_clients.remove(websocket)
    

@app.websocket("/qa")
async def ask_for_qa(websocket:WebSocket, user_id:str=Query(...)):
    
    try:
        await websocket.accept()
        websocket_clients.append(websocket)
        while True:
            
            message = await websocket.receive_text()
            async for token in openai_qa.run_qa_chain(message, user_id):
                await websocket.send_text(token)
    except WebSocketDisconnect:
        logger.info("websocket out")
        # websocket_clients.remove(websocket)
    

if __name__ == "__main__":
    uvicorn.run("main_websocket:app", port=8080)