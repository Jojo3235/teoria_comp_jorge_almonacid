import ply.lex as lex

# Lista de tokens que reconocerá el lexer
tokens = (
    'ABRIR_ETIQUETA',       # <etiqueta
    'CERRAR_ETIQUETA',      # </etiqueta
    'ETIQUETA_AUTOCIERRE',  # <etiqueta ... />
    'FIN_ETIQUETA',         # >
    'NOMBRE_ATRIBUTO',      # nombre de atributos como src, href, etc.
    'IGUAL',                # =
    'VALOR_ATRIBUTO',       # "valor"
    'TEXTO',                # texto libre fuera de etiquetas
)

# Ignorar espacios, tabs, DOCTYPE y comentarios HTML
t_ignore = ' \t'
t_ignore_DOCTYPE = r'<!DOCTYPE[^>]*>'
t_ignore_COMMENT = r'<!--(.|\n)*?-->'

# Reconocer etiquetas autoconclusivas como <img ... />
def t_ETIQUETA_AUTOCIERRE(t):
    r'<[a-zA-Z]+(?:\s+[a-zA-Z_:.-]+(?:\s*=\s*"[^"]*")?)*\s*/>'
    t.value = t.value.lower()
    return t

# Reconocer etiquetas de apertura como <a, <div
def t_ABRIR_ETIQUETA(t):
    r'<[a-zA-Z]+'
    t.value = t.value.lower()
    return t

# Reconocer etiquetas de cierre como </a>
def t_CERRAR_ETIQUETA(t):
    r'</[a-zA-Z]+'
    t.value = t.value.lower()
    return t

# Final de etiqueta >
def t_FIN_ETIQUETA(t):
    r'>'
    return t

# Atributos típicos en HTML
def t_NOMBRE_ATRIBUTO(t):
    r'(href|src|alt|title|width|height|target|rel|class|id|style|lang)'
    return t

# Símbolo igual entre atributo y valor
def t_IGUAL(t):
    r'='
    return t

# Valor de un atributo entre comillas dobles
def t_VALOR_ATRIBUTO(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # elimina las comillas
    return t

# Texto fuera de etiquetas
def t_TEXTO(t):
    r'[^<]+'
    return t

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()
