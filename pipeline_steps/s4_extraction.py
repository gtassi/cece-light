import json
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel
import prompts
from utils.invoke_llm import invoke_llm, ChatCompletionRequest, ChatMessage


async def s4_extraction(
    base_url: str,
    api_key_env_var: Optional[str],
    llm_model: str,
    ontology: Dict[str, Type[BaseModel]],
    previous_summary: str,
    current_chunk: str,
) -> List[Any]:
    system_message = prompts.s4_extraction
    schema_definitions = {}
    for name, model in ontology.items():
        schema_definitions[name] = model.model_json_schema()
    ontology_as_text = json.dumps(schema_definitions, indent=2)
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
### Ontology:
{0}
### Previous Summary:
{1}
### Current Chunk: 
{2}
                            """.format(
                        ontology_as_text, previous_summary, current_chunk
                    ),
                ),
            ],
        ),
    )
    return json.loads(llm_response.choices[0].message.content or "[]")
