from jinja2 import Environment, FileSystemLoader

jinja_env = Environment(loader=FileSystemLoader("prompts"), autoescape=False)
