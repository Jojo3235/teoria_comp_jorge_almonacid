import os
import re
import lexer
import parser as my_parser
from bs4 import BeautifulSoup
import requests
from collections import Counter

def extraer_urls(data):
    lexer.lexer.input(data)
    my_parser.parser.parse(data)
    return my_parser.urls_links, my_parser.urls_images


def esta_balanceado(data):
    stack = []
    tags = re.findall(r'</?\w+[^>]*>', data)

    for tag in tags:
        if not tag.startswith('</'):
            tagname = re.match(r'<(\w+)', tag).group(1)
            if tagname.lower() not in ['img', 'br', 'hr', 'meta', 'input']:
                stack.append(tagname.lower())
        else:
            tagname = re.match(r'</(\w+)', tag).group(1)
            if not stack or stack[-1] != tagname.lower():
                return False
            stack.pop()

    return len(stack) == 0


def analizar_con_bs4(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = [a.get('href') for a in soup.find_all('a', href=True)]
    images = [img.get('src') for img in soup.find_all('img', src=True)]

    etiquetas = ['a', 'img', 'br', 'div', 'li', 'ul', 'p', 'span', 'table', 'td', 'tr']
    conteo = Counter()
    for tag in etiquetas:
        conteo[tag] = len(soup.find_all(tag))

    # Guardar resultados
    with open('bs4_urls_enlaces.txt', 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')

    with open('bs4_urls_imagenes.txt', 'w', encoding='utf-8') as f:
        for img in images:
            f.write(img + '\n')

    print("Estadísticas de etiquetas HTML:")
    for tag, count in conteo.items():
        print(f"{tag}: {count}")


def main():
    archivo_html = 'test_page.html'

    if not os.path.exists(archivo_html):
        print(f"No se encontró el archivo {archivo_html}")
        return

    with open(archivo_html, 'r', encoding='utf-8') as f:
        data = f.read()

    links, images = extraer_urls(data)

    with open('urls_enlaces.txt', 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')

    with open('urls_imagenes.txt', 'w', encoding='utf-8') as f:
        for img in images:
            f.write(img + '\n')

    print(f"Enlaces encontrados: {len(links)}")
    print(f"Imágenes encontradas: {len(images)}")

    if esta_balanceado(data):
        print("El documento HTML está balanceado.")
    else:
        print("El documento HTML NO está balanceado.")

    url_real = 'https://www.python.org'
    analizar_con_bs4(url_real)


if __name__ == '__main__':
    main()