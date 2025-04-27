import ply.yacc as yacc
from lexer import tokens

urls_links = []
urls_images = []


def p_html(p):
    '''html : elementos'''
    pass


def p_elementos(p):
    '''elementos : elemento elementos
                 | elemento'''
    pass


def p_elemento(p):
    '''elemento : link
                | image'''
    pass


def p_link(p):
    'link : A_OPEN A_CLOSE'
    # Extraer URL del token A_OPEN
    import re
    href = re.search(r'href=["\']([^"\']+)', p[1])
    if href:
        urls_links.append(href.group(1))


def p_image(p):
    'image : IMG'
    # Extraer URL del token IMG
    import re
    src = re.search(r'src=["\']([^"\']+)', p[1])
    if src:
        urls_images.append(src.group(1))


def p_error(p):
    pass

parser = yacc.yacc()