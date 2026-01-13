import json
from typing import AsyncGenerator, Optional, cast
import prompts
from utils.invoke_llm import invoke_llm, ChatCompletionRequest, ChatMessage
from utils.render_template import render_template


async def s2_chunking(
    base_url: str,
    api_key_env_var: Optional[str],
    llm_model: str,
    text: str,
    chunk_size: int,
    chunk_macro_size: int,
) -> AsyncGenerator[str, None]:
    system_message = render_template(prompts.s2_chunking, {"chunk_size": chunk_size})
    while len(text) > 0:
        macro_chunk = text[:chunk_macro_size]
        text = text[chunk_macro_size:]
        llm_response = await invoke_llm(
            base_url,
            api_key_env_var,
            ChatCompletionRequest(
                model=llm_model,
                messages=[
                    ChatMessage(role="system", content=system_message),
                    ChatMessage(role="user", content=macro_chunk),
                ],
            ),
        )
        chunks = cast(
            list[str],
            json.loads(llm_response.choices[0].message.content),
        )
        residue = chunks.pop() if len(text) > 0 else ""
        text = residue + text
        for chunk in chunks:
            yield chunk
