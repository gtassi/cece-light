from typing import Any, Dict
from jinja2 import Environment, Template


jinja2_environment: Environment = Environment(keep_trailing_newline=True)
template_cache: Dict[str, Template] = {}


def render_template(template_str: str, context: Dict[str, Any]) -> str:
    if template_str not in template_cache:
        template_cache[template_str] = jinja2_environment.from_string(template_str)
    template = template_cache[template_str]
    return template.render(context)
