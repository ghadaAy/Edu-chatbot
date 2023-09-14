from __future__ import annotations

import asyncio
from typing import Any, Union
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema.output import LLMResult

# TODO If used by two LLM runs in parallel this won't work as expected


class EnqueueCallbackHandler(AsyncCallbackHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    @property
    def always_verbose(self) -> bool:
        return True

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        await self.queue.put(token)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        await self.queue.put(None)

    async def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        await self.queue.put(None)


    # TODO implement the other methods

   