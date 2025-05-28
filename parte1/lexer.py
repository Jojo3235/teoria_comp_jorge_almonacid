import ply.lex as lex

# Lista de tokens
tokens = (
    'ABRIR_ETIQUETA',
    'CERRAR_ETIQUETA',
    'ETIQUETA_AUTOCIERRE',
    'FIN_ETIQUETA',
    'NOMBRE_ATRIBUTO',
    'IGUAL',
    'VALOR_ATRIBUTO',
    'TEXTO',
)

# Ignorar espacios, tabs, DOCTYPE y comentarios
t_ignore = ' \t'
t_ignore_DOCTYPE = r'<!DOCTYPE[^>]*>'
t_ignore_COMMENT = r'<!--(.|\n)*?-->'

# Etiqueta autoconclusiva: <img ... />
def t_ETIQUETA_AUTOCIERRE(t):
    r'<[a-zA-Z]+(?:\s+[a-zA-Z_:.-]+(?:\s*=\s*"[^"]*")?)*\s*/>'
    t.value = t.value.lower()
    return t

# Etiqueta de apertura: <a, <div, <p, etc.
def t_ABRIR_ETIQUETA(t):
    r'<[a-zA-Z]+'
    t.value = t.value.lower()
    return t

# Etiqueta de cierre: </a, </p, etc.
def t_CERRAR_ETIQUETA(t):
    r'</[a-zA-Z]+'
    t.value = t.value.lower()
    return t

# Fin de una etiqueta normal: >
def t_FIN_ETIQUETA(t):
    r'>'
    return t

# Nombre de atributos comunes
def t_NOMBRE_ATRIBUTO(t):
    r'(href|src|alt|title|width|height|target|rel|class|id|style|lang)'
    return t

# Igual entre atributo y valor
def t_IGUAL(t):
    r'='
    return t

# Valor de atributo entre comillas dobles
def t_VALOR_ATRIBUTO(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # elimina las comillas
    return t

# Texto fuera de etiquetas
def t_TEXTO(t):
    r'[^<]+'
    return t

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()
