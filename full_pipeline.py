from typing import Any, List, Optional
from pipeline_steps.s0_ttl_to_pydantic import s0_ttl_to_pydantic
from pipeline_steps.s2_chunking import s2_chunking
from pipeline_steps.s3_summarization import s3_summarization
from pipeline_steps.s4_extraction import s4_extraction
from pipeline_steps.s6_accumulation import s6_accumulation


async def full_pipeline(
    base_url: str,
    api_key_env_var: Optional[str],
    llm_model: str,
    chunk_size: int,
    chunk_macro_size: int,
    summary_size: int,
    ontology_definition: str,
    document: str,
):
    ontology = s0_ttl_to_pydantic(ontology_definition)

    previous_summary = " "
    previous_entities: List[Any] = []
    i = 0
    chunks = s2_chunking(
        base_url,
        api_key_env_var,
        llm_model,
        document,
        chunk_size,
        chunk_macro_size,
    )
    async for current_chunk in chunks:
        current_entities = await s4_extraction(
            base_url,
            api_key_env_var,
            llm_model,
            ontology,
            previous_summary,
            current_chunk,
        )
        previous_summary = await s3_summarization(
            base_url,
            api_key_env_var,
            llm_model,
            previous_summary,
            current_chunk,
            summary_size,
        )
        previous_entities = await s6_accumulation(
            base_url,
            api_key_env_var,
            llm_model,
            ontology,
            previous_entities,
            current_entities,
        )
        i += 1
        print(f"Entities {i}: {previous_entities}")
    return previous_entities
