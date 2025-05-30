import ply.yacc as yacc  # Importa el módulo yacc de PLY para construir el parser
from lexer import tokens  # Importa los tokens definidos en el archivo lexer.py

# Variables globales para almacenar resultados extraídos del HTML
urls_links = []               # Lista de URLs de hipervínculos (<a href="...">)
urls_images = []             # Lista de URLs de imágenes (<img src="...">)
encuentros_etiquetas = set()  # Conjunto de tipos de etiquetas HTML encontradas

# Regla inicial del parser: comienza a analizar desde la producción 'html'
def p_html(p):
    '''html : elementos'''  # Un documento HTML consiste en una serie de elementos
    pass

# Regla para definir múltiples elementos HTML, uno seguido de otro
def p_elementos(p):
    '''elementos : elemento elementos
                 | elemento'''  # Un grupo de elementos puede ser recursivo o uno solo
    pass

# Regla para manejar una etiqueta con apertura y cierre (ej: <div> ... </div>)
def p_elemento_etiqueta_abre(p):
    'elemento : ABRIR_ETIQUETA atributos FIN_ETIQUETA elementos CERRAR_ETIQUETA'
    tag = p[1][1:].lower()  # Elimina el carácter '<' y convierte a minúsculas
    encuentros_etiquetas.add(tag)  # Registra el tipo de etiqueta encontrado

# Regla para manejar etiquetas autoconclusivas (ej: <img ... />)
def p_elemento_autocierre(p):
    'elemento : ETIQUETA_AUTOCIERRE'
    tag = p[1][1:].split()[0].lower()  # Extrae el nombre de la etiqueta y convierte a minúsculas
    encuentros_etiquetas.add(tag)  # Registra la etiqueta como encontrada

# Regla para manejar bloques de texto plano entre etiquetas
def p_elemento_texto(p):
    'elemento : TEXTO'
    pass  # No se realiza acción con el texto plano, solo se reconoce

# Regla para permitir múltiples atributos dentro de una etiqueta o ninguno
def p_atributos(p):
    '''atributos : atributo atributos
                 | atributo
                 | '''  # Atributos pueden ser múltiples, uno solo o ningún atributo
    pass

# Regla para manejar un atributo con nombre, signo igual y valor
def p_atributo(p):
    'atributo : NOMBRE_ATRIBUTO IGUAL VALOR_ATRIBUTO'
    nombre = p[1].lower()  # Convierte el nombre del atributo a minúsculas
    valor = p[3]           # Valor del atributo entre comillas
    # Clasificación especial de atributos relevantes
    if nombre == 'href':
        urls_links.append(valor)  # Añade al listado de enlaces
    elif nombre == 'src':
        urls_images.append(valor)  # Añade al listado de imágenes

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"[ERROR] Simbolo inesperado: {p}")  # Si hay token inesperado
    else:
        print("[ERROR] Fin inesperado del archivo")  # Si el archivo termina inesperadamente

# Construcción final del parser utilizando PLY
parser = yacc.yacc()
