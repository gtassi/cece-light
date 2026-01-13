import asyncio
from typing import Optional
from pydantic import BaseModel, Field
import yaml
from full_pipeline import full_pipeline


class Config(BaseModel):
    base_url: str
    api_key_env_var: Optional[str] = Field(default=None)
    llm_model: str
    chunk_size: int
    chunk_macro_size: int
    summary_size: int


def main():
    configuration_file = "config.yml"
    test_ontology_definition_file = "tests/clinical.ttl"
    test_document_file = "tests/clinical_01.txt"

    with open(configuration_file, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)
    with open(test_ontology_definition_file, "r", encoding="utf-8") as f:
        test_ontology_definition = f.read()
    with open(test_document_file, "r", encoding="utf-8") as f:
        test_document = f.read()

    config = Config.model_validate(raw_config)

    asyncio.run(
        full_pipeline(
            config.base_url,
            config.api_key_env_var,
            config.llm_model,
            config.chunk_size,
            config.chunk_macro_size,
            config.summary_size,
            test_ontology_definition,
            test_document,
        )
    )


if __name__ == "__main__":
    main()
