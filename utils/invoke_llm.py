import os
from typing import List, Literal, Optional
from httpx import AsyncClient, HTTPStatusError
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Optional[Literal["system", "user", "assistant", "tool"]] = None
    content: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    model: str


class Choice(BaseModel):
    message: ChatMessage


class ChatCompletionResponse(BaseModel):
    choices: List[Choice]


async def invoke_llm(
    base_url: str,
    api_key_env_var: Optional[str],
    request: ChatCompletionRequest,
) -> ChatCompletionResponse:
    http_client = AsyncClient(timeout=300.0)
    response = await http_client.post(
        base_url + "/chat/completions",
        headers={
            **(
                {"Authorization": "Bearer " + os.environ.get(api_key_env_var, "")}
                if api_key_env_var
                else {}
            ),
            "Content-Type": "application/json",
        },
        json=request.model_dump(),
    )
    try:
        response.raise_for_status()
    except HTTPStatusError as e:
        print(
            f"Service call responded with error: {e.response.status_code} - {e.response.text}"
        )
        raise

    return ChatCompletionResponse.model_validate(response.json())
