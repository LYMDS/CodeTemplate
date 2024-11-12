from jinja2 import nodes
from jinja2.ext import Extension

class CustomVariableExtension(Extension):
    tags = {'variable'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        name = parser.parse_assign_target()
        value = parser.parse_expression()
        body = parser.parse_statements(['name:endvariable'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_render_variable', [name, value]), [], [], body).set_lineno(lineno)

    def _render_variable(self, name, value, caller):
        return f"<span style='color: blue'>{name}={value}</span>"




