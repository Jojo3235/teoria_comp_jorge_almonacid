import ply.lex as lex

# Lista de tokens necesarios para el parser
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

# Ignorar espacios, tabs, comentarios y declaraciones DOCTYPE
t_ignore = ' \t'
t_ignore_DOCTYPE = r'<!DOCTYPE[^>]*>'
t_ignore_COMMENT = r'<!--(.|\n)*?-->'

# Etiqueta autoconclusiva: <img ... />
def t_ETIQUETA_AUTOCIERRE(t):
    r'<[a-zA-Z]+(?:\s+[a-zA-Z_:.-]+\s*=\s*"[^"]*")*\s*/\s*>'
    t.value = t.value.lower()
    return t

# Etiqueta de apertura: <div, <p, etc.
def t_ABRIR_ETIQUETA(t):
    r'<[a-zA-Z]+'
    t.value = t.value.lower()
    return t

# Etiqueta de cierre: </div, </p, etc.
def t_CERRAR_ETIQUETA(t):
    r'</[a-zA-Z]+'
    t.value = t.value.lower()
    return t

# Fin de etiqueta: >
def t_FIN_ETIQUETA(t):
    r'>'
    return t

# Atributo de una etiqueta HTML
def t_NOMBRE_ATRIBUTO(t):
    r'[a-zA-Z_:.-]+'
    return t

# Igual entre atributo y valor
def t_IGUAL(t):
    r'='
    return t

# Valor de atributo entre comillas
def t_VALOR_ATRIBUTO(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # elimina las comillas
    return t

# Texto libre entre etiquetas
def t_TEXTO(t):
    r'[^<]+'
    return t

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errores léxicos
def t_error(t):
    print(f"Caracter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción final del lexer
lexer = lex.lex()
