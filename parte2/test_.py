import os
import pytest
from main import analizar_con_parser, esta_balanceado, guardar_resultados, urls_links, urls_images, encuentros_etiquetas

PRUEBA1 = "test files/prueba1.html"
PRUEBA2 = "test files/prueba2.html"
PRUEBA4 = "test files/prueba4.html"

@pytest.fixture(autouse=True)
def limpiar_resultados():
    urls_links.clear()
    urls_images.clear()
    encuentros_etiquetas.clear()
    archivos = ["urls_enlaces_parser.txt", "urls_imagenes_parser.txt"]
    yield
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)

def cargar_html(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

def test_prueba1_no_enlaces_no_imagenes():
    html = cargar_html(PRUEBA1)
    analizar_con_parser(html)
    assert urls_links == []
    assert urls_images == []
    assert esta_balanceado(html) is True

def test_prueba2_enlaces_e_imagenes_validos():
    html = cargar_html(PRUEBA2)
    analizar_con_parser(html)
    assert "http://www.bbc.co.uk" in urls_links
    assert "brushedsteel.jpg" in urls_images
    assert "a" in encuentros_etiquetas
    assert "img" in encuentros_etiquetas
    assert esta_balanceado(html) is True

def test_prueba4_balanceo_y_trampa():
    html = cargar_html(PRUEBA4)
    analizar_con_parser(html)
    # Solo debe capturar los href válidos
    assert "http://www.bbc.co.uk" in urls_links
    assert "este href no es de etiqueta A" not in urls_links
    assert "esto es una trampa" not in urls_images
    assert esta_balanceado(html) is False

def test_guardado_correcto():
    html = cargar_html(PRUEBA2)
    analizar_con_parser(html)
    guardar_resultados("urls_enlaces_parser.txt", urls_links)
    guardar_resultados("urls_imagenes_parser.txt", urls_images)

    assert os.path.exists("urls_enlaces_parser.txt")
    assert os.path.exists("urls_imagenes_parser.txt")

    with open("urls_enlaces_parser.txt", encoding="utf-8") as f:
        contenido = f.read()
        assert "http://www.bbc.co.uk" in contenido

    with open("urls_imagenes_parser.txt", encoding="utf-8") as f:
        contenido = f.read()
        assert "brushedsteel.jpg" in contenido

def test_trampa_manual_inline():
    html = '<html><body><p>href="trampa"</p><a href="example.com">ejemplo</a></body></html>'
    analizar_con_parser(html)
    assert "example.com" in urls_links
    assert "trampa" not in urls_links
    assert esta_balanceado(html) is True
