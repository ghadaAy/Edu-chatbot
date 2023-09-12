from langchain.callbacks.base import BaseCallbackHandler

class ChainCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = []

    def on_llm_new_token(self, token, **kwargs) -> None:
        self.tokens.append(token)
    def on_llm_end(self):
        self.tokens = []