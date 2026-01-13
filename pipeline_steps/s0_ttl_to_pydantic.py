from typing import Any, Type, Dict, Optional, List
from pydantic import BaseModel, Field, create_model
from rdflib import Graph, RDF, RDFS, OWL, Namespace


def s0_ttl_to_pydantic(ttl_content: str) -> Dict[str, Type[BaseModel]]:
    graph = Graph()
    graph.parse(data=ttl_content, format="turtle")

    models: Dict[str, Type[BaseModel]] = {}

    classes = list(graph.subjects(RDF.type, OWL.Class)) + list(
        graph.subjects(RDF.type, RDFS.Class)
    )

    for cls in classes:
        class_name = _clean_name(cls)
        models[class_name] = create_model(class_name, __base__=BaseModel)

    for cls in classes:
        class_name = _clean_name(cls)
        fields: Dict[str, Any] = {}

        for prop_uri in graph.subjects(RDFS.domain, cls):
            prop_name = _clean_name(prop_uri)
            range_uri = graph.value(prop_uri, RDFS.range)
            description = graph.value(prop_uri, RDFS.comment) or graph.value(
                prop_uri, RDFS.label
            )

            base_type = _get_custom_type(range_uri, models)

            is_functional = (prop_uri, RDF.type, OWL.FunctionalProperty) in graph

            if is_functional:
                field_type = Optional[base_type]
                field_def = Field(
                    None, description=str(description) if description else None
                )
            else:
                field_type = Optional[List[base_type]]
                field_def = Field(
                    default_factory=list,
                    description=str(description) if description else None,
                )

            fields[prop_name] = (field_type, field_def)

        models[class_name] = create_model(class_name, **fields, __base__=BaseModel)

    for model in models.values():
        model.model_rebuild()

    return models


def _clean_name(uri: Any) -> str:
    if not uri:
        return "Unknown"
    return str(uri).split("#")[-1].split("/")[-1]


def _get_custom_type(range_uri: Any, models: Dict[str, Type[BaseModel]]) -> Any:
    XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
    mapping: Dict[str, Any] = {
        str(XSD.string): str,
        str(XSD.decimal): float,
        str(XSD.integer): int,
        str(XSD.boolean): bool,
        str(XSD.dateTime): str,
    }
    if not range_uri:
        return Any
    uri_str = str(range_uri)
    if uri_str in mapping:
        return mapping[uri_str]

    range_name = _clean_name(range_uri)
    return models.get(range_name, Any)
