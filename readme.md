# Ontology-Guided Information Extraction Pipeline

This project implements a lightweight, modular pipeline that transforms unstructured text into structured, semantically consistent knowledge representations. By using **OWL/RDFS Ontologies** as structural "guardrails," the system ensures that Large Language Model (LLM) extractions are traceable, validated, and interoperable.

## Architecture Overview

The pipeline follows a multi-stage process to maintain context and ensure data integrity:

1.  **S0: Ontology Interpretation**: Converts Turtle (`.ttl`) definitions into dynamic Pydantic models at runtime.
2.  **S2: Semantic Chunking**: Splits long documents into coherent pieces based on LLM decision-making.
3.  **S3: Rolling Summarization**: Maintains a recursive summary to provide the LLM with context from previous chunks.
4.  **S4: Structured Extraction**: Uses the Pydantic-generated JSON Schema to guide the LLM in identifying entities and relations.
5.  **S6: Entity Accumulation**: Merges new extractions with existing ones, resolving duplicates and updating properties.



## 🛠 Key Components

### Dynamic Schema Mapping (`s0_ttl_to_pydantic.py`)
This module is the backbone of the "Ontology-Guided" approach. It parses RDF/OWL classes and properties to create Python class hierarchies automatically.
* **Relationship Handling**: Distinguishes between `FunctionalProperties` (single values) and standard properties (lists).
* **Metadata Preservation**: Maps `rdfs:comment` and `rdfs:label` to Pydantic field descriptions to act as instructions for the LLM.
* **Type Safety**: Maps XML Schema (XSD) types to native Python types for validation.

### Context Management (`s2_chunking.py` & `s3_summarization.py`)
To handle long documents, the pipeline uses:
* **Macro-Micro Chunking**: Takes a fixed-length portion of text and lets the LLM decide the best semantic split points.
* **Recursive Summarization**: An incremental state that combines the previous summary with the new chunk to preserve information.

### Knowledge Consolidation (`s6_accumulation.py`)
Since entities may appear across multiple chunks, this stage performs **Entity Resolution**. It identifies overlapping entities and applies logic to merge properties (e.g., preferring non-null values or fuzzy matching).



## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Dependencies: `httpx`, `jinja2`, `pydantic`, `rdflib`, and an LLM provider (e.g., OpenAI, Anthropic, or Local via Ollama).

### Running the Pipeline
The core execution is managed by `full_pipeline.py`, which orchestrates the sequence from the ontology definition to the final accumulated entities.

## 📚 Didactic Note
This project is intended for educational purposes. Step **S5: Grounding** (removing hallucinations and ensuring traceability back to source text) is intentionally left as an exercise for participants.