from jinja2 import Environment, FileSystemLoader
from pathlib import Path

env = Environment(
    loader=FileSystemLoader(searchpath=Path(__file__).parent)
)


def get_instructions():
    return get_prompt("instructions.j2")


def get_output_summary():
    return get_prompt("output.j2")


def get_prompt(file_name: str, **options) -> str:    
    template_file = env.get_template(file_name)  
    output = template_file.render()  
    return output