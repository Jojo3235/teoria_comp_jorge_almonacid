import requests
from lexer import lexer
from parser import parser, urls_links, urls_images, encuentros_etiquetas
import re
from collections import Counter

# Obtiene el HTML crudo desde una URL usando requests
# Devuelve el contenido HTML como texto plano
def obtener_html_raw(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; WebScraper/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] no se pudo acceder a {url}: {e}")
        return ""

# Comprueba si el HTML está balanceado en cuanto a etiquetas
# Ignora etiquetas autocontenidas como <img>, <br>, etc.
def esta_balanceado(data):
    stack = []
    autocontenidas = {'img', 'br', 'hr', 'meta', 'input', 'link', 'source', 'track', 'wbr'}
    tags = re.findall(r'<(/?)(\w+)[^>]*>', data)

    for cierre, nombre in tags:
        nombre = nombre.lower()
        if nombre in autocontenidas:
            continue
        if cierre:
            if not stack or stack[-1] != nombre:
                return False
            stack.pop()
        else:
            stack.append(nombre)
    return len(stack) == 0

# Procesa el HTML con el analizador léxico y sintáctico (parser)
# Recolecta enlaces, imágenes y tipos de etiquetas presentes en el documento
def analizar_con_parser(html):
    urls_links.clear()
    urls_images.clear()
    encuentros_etiquetas.clear()
    lexer.input(html)
    parser.parse(html)

    # Refuerzo: detectar imágenes por expresión regular si el parser no las detecta
    posibles_imgs = re.findall(r'<img[^>]*src="([^"]+)"', html)
    for src in posibles_imgs:
        if src not in urls_images:
            urls_images.append(src)
        encuentros_etiquetas.add('img')

    # Refuerzo: detectar todos los tipos de etiquetas del HTML (incluso no manejadas por el parser)
    all_tags = re.findall(r'<\/?(\w+)', html)
    for tag in all_tags:
        encuentros_etiquetas.add(tag.lower())

# Guarda una lista de resultados (enlaces o imágenes) en un archivo de texto plano
def guardar_resultados(nombre, lista):
    with open(nombre, "w", encoding="utf-8") as f:
        for item in lista:
            f.write(item + "\n")

# Función principal: descarga el HTML, lo analiza, imprime y guarda resultados
def main():
    
    url = "https://www.python.org"
    html = obtener_html_raw(url)
    
    # Lee el HTML desde un archivo local
    # with open("test files/prueba6.html", "r", encoding="utf-8") as f:
        # html = f.read()

    if not html:
        print("[ERROR] archivo vacio o no cargado")
        return

    analizar_con_parser(html)

    print(f"\n[Enlaces encontrados]: {len(urls_links)}")
    for link in urls_links:
        print(f"  - {link}")

    print(f"\n[Imagenes encontradas]: {len(urls_images)}")
    for img in urls_images:
        print(f"  - {img}")

    print(f"\n[Tipos de etiquetas encontradas]: {len(encuentros_etiquetas)}")
    for etq in sorted(encuentros_etiquetas):
        print(f"  - {etq}")

    guardar_resultados("urls_enlaces_parser.txt", urls_links)
    guardar_resultados("urls_imagenes_parser.txt", urls_images)

    if esta_balanceado(html):
        print("\nEl documento HTML esta balanceado.")
    else:
        print("\nEl documento HTML no esta balanceado.")


# Punto de entrada del script
if __name__ == "__main__":
    main()
