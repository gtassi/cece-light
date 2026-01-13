from typing import Optional
import prompts
from utils.invoke_llm import invoke_llm, ChatCompletionRequest, ChatMessage
from utils.render_template import render_template


async def s3_summarization(
    base_url: str,
    api_key_env_var: Optional[str],
    llm_model: str,
    previous_summary: str,
    current_chunk: str,
    summary_size: int,
) -> str:
    system_message = render_template(
        prompts.s3_summarization, {"summary_size": summary_size}
    )
    llm_response = await invoke_llm(
        base_url,
        api_key_env_var,
        ChatCompletionRequest(
            model=llm_model,
            messages=[
                ChatMessage(role="system", content=system_message),
                ChatMessage(
                    role="user",
                    content="""
### Previous Summary:
{0}
### Current Chunk: 
{1}
                            """.format(
                        previous_summary, current_chunk
                    ),
                ),
            ],
        ),
    )
    new_summary = llm_response.choices[0].message.content or ""
    return new_summary
