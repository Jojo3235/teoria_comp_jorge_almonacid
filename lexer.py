import ply.lex as lex

# Lista de tokens
tokens = (
    'ABRIR_ETIQUETA',
    'CERRAR_ETIQUETA',
    'FIN_ETIQUETA',
    'NOMBRE_ATRIBUTO',
    'IGUAL',
    'VALOR_ATRIBUTO',
    'TEXTO',
)

# Ignorar espacios, tabs, comentarios y DOCTYPE
t_ignore = ' \t'
t_ignore_COMMENT = r'<!--.*?-->'
t_ignore_DOCTYPE = r'<!DOCTYPE.*?>'

# Etiquetas como <a, <img, <div...
def t_ABRIR_ETIQUETA(t):
    r'<[a-zA-Z]+'
    return t

# Etiquetas de cierre como </a, </div...
def t_CERRAR_ETIQUETA(t):
    r'</[a-zA-Z]+'
    return t

# Etiquetas autoconclusivas: />
def t_FIN_ETIQUETA_AUTOCIERRE(t):
    r'/>'  # debe ir antes que '>'
    t.type = 'FIN_ETIQUETA'
    return t

# Cierre normal de etiqueta: >
def t_FIN_ETIQUETA(t):
    r'>'
    return t

# Atributos comunes
def t_NOMBRE_ATRIBUTO(t):
    r'(href|src|alt|title|width|height|target|rel|class|id|style)'
    return t

def t_IGUAL(t):
    r'='
    return t

# Valor de atributos entre comillas
def t_VALOR_ATRIBUTO(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]  # elimina comillas
    return t

# Nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Cualquier texto fuera de etiquetas
def t_TEXTO(t):
    r'[^<]+'
    return t

# Caracteres ilegales
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()
