import ply.lex as lex

# Lista de tokens
tokens = (
    'A_OPEN',
    'A_CLOSE',
    'IMG',
)

# Expresiones regulares para tokens
t_A_OPEN = r'<a\s+[^>]*href=["\'][^"\']+["\'][^>]*>'
t_A_CLOSE = r'</a>'
t_IMG = r'<img\s+[^>]*src=["\'][^"\']+["\'][^>]*>'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()