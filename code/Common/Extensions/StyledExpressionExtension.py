from jinja2 import Environment, FileSystemLoader, nodes
from jinja2.ext import Extension
from jinja2.lexer import Token,TokenStream

class StyledExpressionExtension(Extension):
    def filter_stream(self, stream):
        for token in stream:
            if token.type == 'variable_begin':
                yield token
                token = next(stream)
                yield token
            else:
                yield token

