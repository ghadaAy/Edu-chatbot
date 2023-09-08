from venv import logger
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.schema  import User
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

@app.websocket("/ws")
async def ask_for_summarization(websocket:WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            async for token in openai_summarizing.answer(message):
                await websocket.send_text(token)
    except WebSocketDisconnect:
        logger.info("websocket out")
        # websocket_clients.remove(websocket)
    

if __name__ == "__main__":
    uvicorn.run("main_websocket:app", port=8080)



