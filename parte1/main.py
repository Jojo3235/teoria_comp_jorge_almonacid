import lexer  # Importa el analizador léxico personalizado
import os     # Para manejar rutas de archivos
import re     # Expresiones regulares para búsquedas de patrones

# Función principal que analiza un archivo HTML y extrae URLs e imágenes válidas
def analizar_html(ruta_html, salida_urls):
    # Lee el contenido del archivo HTML en texto plano
    with open(ruta_html, "r", encoding="utf-8") as f:
        data = f.read()

    # Introduce el contenido HTML al lexer para comenzar el análisis
    lexer.lexer.input(data)

    # Inicializa estructuras auxiliares
    tag_stack = []                # Pila para comprobar el balanceo de etiquetas
    enlaces = []                  # Lista de enlaces (href) válidos
    imagenes = []                 # Lista de imágenes (src) válidas
    etiqueta_actual = None        # Etiqueta que se está analizando
    atributos_en_etiqueta = {}    # Diccionario de atributos de la etiqueta actual
    dentro_etiqueta = False       # Indica si estamos dentro de una etiqueta abierta
    etiqueta_abierta = None       # Guarda la última etiqueta abierta
    documento_balanceado = True   # Flag para balanceo de etiquetas

    # Lista de etiquetas HTML5 que se autoconcluyen y no requieren cierre
    autocontenidas_html5 = {'area', 'base', 'br', 'col', 'embed', 'hr',
                            'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

    # Comienza el análisis léxico, token por token
    while True:
        tok = lexer.lexer.token()
        if not tok:
            break

        # Caso 1: Etiqueta autoconclusiva (ej. <img ... />)
        if tok.type == 'ETIQUETA_AUTOCIERRE':
            etiqueta = tok.value[1:].split()[0].replace('/', '')  # obtiene el nombre de la etiqueta
            attrs = re.findall(r'(href|src)\s*=\s*"([^"]+)"', tok.value)  # busca atributos válidos
            for attr, val in attrs:
                if attr == 'href' and etiqueta == 'a':
                    enlaces.append(val)
                elif attr == 'src' and etiqueta == 'img':
                    imagenes.append(val)

        # Caso 2: Etiqueta de apertura (ej. <a)
        elif tok.type == 'ABRIR_ETIQUETA':
            etiqueta_actual = tok.value[1:]
            etiqueta_abierta = etiqueta_actual
            atributos_en_etiqueta = {}
            dentro_etiqueta = True
            # Solo añadir a la pila si no es autocontenida
            if etiqueta_actual not in autocontenidas_html5:
                tag_stack.append(etiqueta_actual)

        # Caso 3: Fin de etiqueta (ej. >)
        elif tok.type == 'FIN_ETIQUETA':
            dentro_etiqueta = False

        # Caso 4: Etiqueta de cierre (ej. </a)
        elif tok.type == 'CERRAR_ETIQUETA':
            cerrar = tok.value[2:]
            dentro_etiqueta = False

            # Añade enlaces o imágenes solo si se cerró correctamente
            if cerrar == 'a' and 'href' in atributos_en_etiqueta:
                enlaces.append(atributos_en_etiqueta['href'])
            elif cerrar == 'img' and 'src' in atributos_en_etiqueta:
                imagenes.append(atributos_en_etiqueta['src'])

            # Comprobación de balanceo de etiquetas
            if tag_stack:
                if cerrar in tag_stack:
                    while tag_stack and tag_stack[-1] != cerrar:
                        etiqueta_erronea = tag_stack.pop()
                        print(f"[ERROR] Etiqueta sin cerrar antes de cerrar {cerrar}: {etiqueta_erronea}")
                        documento_balanceado = False
                    tag_stack.pop()
                else:
                    print(f"[ERROR] Cierre inesperado de etiqueta: {cerrar}")
                    documento_balanceado = False
            else:
                print(f"[ERROR] Cierre inesperado de etiqueta: {cerrar}")
                documento_balanceado = False

            # Reinicia variables auxiliares
            etiqueta_actual = None
            atributos_en_etiqueta = {}
            etiqueta_abierta = None

        # Caso 5: Atributos de una etiqueta (ej. href="...")
        elif tok.type == 'NOMBRE_ATRIBUTO' and dentro_etiqueta:
            attr = tok.value
            igual = lexer.lexer.token()  # Consume el "="
            val = lexer.lexer.token()    # Consume el valor del atributo
            if val and val.type == 'VALOR_ATRIBUTO':
                atributos_en_etiqueta[attr] = val.value
                if etiqueta_abierta == 'a' and attr == 'href':
                    enlaces.append(val.value)
                elif etiqueta_abierta == 'img' and attr == 'src':
                    imagenes.append(val.value)

    # Elimina duplicados preservando el orden
    enlaces = list(dict.fromkeys(enlaces))
    imagenes = list(dict.fromkeys(imagenes))

    # Escribe resultados en archivo de texto
    with open(salida_urls, "w", encoding="utf-8") as out:
        out.write("[Enlaces detectados]\n")
        for url in enlaces:
            out.write(f"{url}\n")
        out.write("\n[Imagenes detectadas]\n")
        for img in imagenes:
            out.write(f"{img}\n")

    # Imprime los resultados por consola
    print("\n[Enlaces detectados]")
    for url in enlaces:
        print(f"  -> {url}")

    print("\n[Imagenes detectadas]")
    for img in imagenes:
        print(f"  -> {img}")

    # Comprobación de balanceo de etiquetas
    if documento_balanceado and not tag_stack:
        print("\nEl documento esta bien balanceado.")
    else:
        print("\nEl documento no esta bien balanceado.")
        if tag_stack:
            print("Etiquetas sin cerrar (desde la mas interna):")
            for tag in reversed(tag_stack):
                print(f"  - {tag}")

# Punto de entrada del script
if __name__ == "__main__":
    ruta_html = os.path.join("tests", "prueba3.html")               # Ruta al archivo de entrada
    salida_urls = os.path.join("tests", "urls_extraidas_3.txt")     # Archivo de salida
    print(f"Analizando archivo: {ruta_html}")
    analizar_html(ruta_html, salida_urls)
    print(f"\nURLs extraidas guardadas en: {salida_urls}")
