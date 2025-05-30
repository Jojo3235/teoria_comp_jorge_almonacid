import lexer
import os
import re

def analizar_html(ruta_html, salida_urls):
    with open(ruta_html, "r", encoding="utf-8") as f:
        data = f.read()

    lexer.lexer.input(data)

    tag_stack = []
    enlaces = []
    imagenes = []
    etiqueta_actual = None
    atributos_en_etiqueta = {}
    dentro_etiqueta = False
    etiqueta_abierta = None
    documento_balanceado = True

    autocontenidas_html5 = {'area', 'base', 'br', 'col', 'embed', 'hr',
                            'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

    while True:
        tok = lexer.lexer.token()
        if not tok:
            break

        if tok.type == 'ETIQUETA_AUTOCIERRE':
            etiqueta = tok.value[1:].split()[0].replace('/', '')
            attrs = re.findall(r'(href|src)\s*=\s*"([^"]+)"', tok.value)
            for attr, val in attrs:
                if attr == 'href' and etiqueta == 'a':
                    enlaces.append(val)
                elif attr == 'src' and etiqueta == 'img':
                    imagenes.append(val)

        elif tok.type == 'ABRIR_ETIQUETA':
            etiqueta_actual = tok.value[1:]
            etiqueta_abierta = etiqueta_actual
            atributos_en_etiqueta = {}
            dentro_etiqueta = True
            if etiqueta_actual not in autocontenidas_html5:
                tag_stack.append(etiqueta_actual)

        elif tok.type == 'FIN_ETIQUETA':
            dentro_etiqueta = False

        elif tok.type == 'CERRAR_ETIQUETA':
            cerrar = tok.value[2:]
            dentro_etiqueta = False

            if cerrar == 'a' and 'href' in atributos_en_etiqueta:
                enlaces.append(atributos_en_etiqueta['href'])
            elif cerrar == 'img' and 'src' in atributos_en_etiqueta:
                imagenes.append(atributos_en_etiqueta['src'])

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

            etiqueta_actual = None
            atributos_en_etiqueta = {}
            etiqueta_abierta = None

        elif tok.type == 'NOMBRE_ATRIBUTO' and dentro_etiqueta:
            attr = tok.value
            igual = lexer.lexer.token()
            val = lexer.lexer.token()
            if val and val.type == 'VALOR_ATRIBUTO':
                atributos_en_etiqueta[attr] = val.value
                if etiqueta_abierta == 'a' and attr == 'href':
                    enlaces.append(val.value)
                elif etiqueta_abierta == 'img' and attr == 'src':
                    imagenes.append(val.value)

    # Eliminar duplicados manteniendo orden (sin usar OrderedDict)
    enlaces = list(dict.fromkeys(enlaces))
    imagenes = list(dict.fromkeys(imagenes))

    with open(salida_urls, "w", encoding="utf-8") as out:
        out.write("[Enlaces detectados]\n")
        for url in enlaces:
            out.write(f"{url}\n")
        out.write("\n[Imagenes detectadas]\n")
        for img in imagenes:
            out.write(f"{img}\n")

    print("\n[Enlaces detectados]")
    for url in enlaces:
        print(f"  -> {url}")

    print("\n[Imagenes detectadas]")
    for img in imagenes:
        print(f"  -> {img}")

    if documento_balanceado and not tag_stack:
        print("\nEl documento esta bien balanceado.")
    else:
        print("\nEl documento no esta bien balanceado.")
        if tag_stack:
            print("Etiquetas sin cerrar (desde la mas interna):")
            for tag in reversed(tag_stack):
                print(f"  - {tag}")

if __name__ == "__main__":
    ruta_html = os.path.join("tests", "prueba3.html")
    salida_urls = os.path.join("tests", "urls_extraidas_3.txt")
    print(f"Analizando archivo: {ruta_html}")
    analizar_html(ruta_html, salida_urls)
    print(f"\nURLs extraidas guardadas en: {salida_urls}")
