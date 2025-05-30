import ply.yacc as yacc
from lexer import tokens

# Variables globales para almacenar resultados
urls_links = []
urls_images = []
encuentros_etiquetas = set()

# Regla de inicio del análisis
def p_html(p):
    '''html : elementos'''
    pass

# Regla para múltiples elementos HTML
def p_elementos(p):
    '''elementos : elemento elementos
                 | elemento'''
    pass

# Manejo de etiquetas con apertura y cierre
def p_elemento_etiqueta_abre(p):
    'elemento : ABRIR_ETIQUETA atributos FIN_ETIQUETA elementos CERRAR_ETIQUETA'
    tag = p[1][1:]  # eliminar '<'
    encuentros_etiquetas.add(tag)

# Manejo de etiquetas autoconclusivas como <img />
def p_elemento_autocierre(p):
    'elemento : ETIQUETA_AUTOCIERRE'
    tag = p[1][1:].split()[0]  # elimina '<' y corta por espacio
    encuentros_etiquetas.add(tag)

# Texto plano
def p_elemento_texto(p):
    'elemento : TEXTO'
    pass

# Múltiples atributos o ninguno
def p_atributos(p):
    '''atributos : atributo atributos
                 | atributo
                 | '''
    pass

# Manejo de atributos
def p_atributo(p):
    'atributo : NOMBRE_ATRIBUTO IGUAL VALOR_ATRIBUTO'
    nombre = p[1].lower()
    valor = p[3]
    if nombre == 'href':
        urls_links.append(valor)
    elif nombre == 'src':
        urls_images.append(valor)

# Manejo de errores
def p_error(p):
    if p:
        print(f"[ERROR] Simbolo inesperado: {p}")
    else:
        print("[ERROR] Fin inesperado del archivo")

# Construcción del parser
parser = yacc.yacc()
