from fastapi import FastAPI, WebSocket
from src.schema  import User
from src.prompts import summarize_prompt, openai_prompt_template
from settings import get_settings
from src.llms.openai import OpenAIManager
from src.prompts import summarize_prompt, openai_prompt_template

app_settings = get_settings()
app = FastAPI()


openai_summarizing = OpenAIManager(prompt=summarize_prompt)
openai_qa = OpenAIManager(prompt=openai_prompt_template)


app = FastAPI()

connected_user = {}
@app.websocket("/add_user/{user_id}")
async def ask_for_summarization(websocket:WebSocket, user:User):
    await websocket.accept()
    connected_user[user.id_] = websocket
    while True:
        message = await websocket.receive_text()
        async for token in openai_summarizing.answer(message):
            await websocket.send_text(token)
        await websocket.close()




