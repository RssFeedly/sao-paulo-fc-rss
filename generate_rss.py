from datetime import datetime, timezone
import re
from xml.etree.ElementTree import Element, SubElement, tostring
import requests

# URL objetivo de la búsqueda de partidos del São Paulo FC en Google
URL = 'https://www.google.com/search?q=partidos+de+sao+paulo+fc&hl=es'

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'es-ES,es;q=0.9',
}


def build_rss_xml(items):
    rss = Element('rss', version='2.0')
    channel = SubElement(rss, 'channel')

    title = SubElement(channel, 'title')
    title.text = 'São Paulo FC - Partidos y Resultados (Google)'

    link = SubElement(channel, 'link')
    link.text = URL

    description = SubElement(channel, 'description')
    description.text = (
        'Feed con los últimos marcadores y próximos partidos del São Paulo FC'
        ' extraídos de Google Partidos.'
    )

    for match in items:
        item = SubElement(channel, 'item')

        item_title = SubElement(item, 'title')
        item_title.text = match['title']

        item_link = SubElement(item, 'link')
        item_link.text = URL

        item_guid = SubElement(item, 'guid')
        item_guid.text = match['guid']

        item_desc = SubElement(item, 'description')
        item_desc.text = match['description']

        item_pubdate = SubElement(item, 'pubDate')
        item_pubdate.text = datetime.now(timezone.utc).strftime(
            '%a, %d %b %Y %H:%M:%S GMT'
        )

    return tostring(rss, encoding='utf-8')


def get_google_matches():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f'Error al conectar con Google: {response.status_code}')
        return []

    html = response.text

    # Extraer bloques de texto relevantes del panel de partidos
    # Buscamos patrones típicos de nombres de equipos e índices numéricos (goles/fechas)
    matches = []

    # Búsqueda limpia de texto dentro del HTML renderizado de Google
    clean_text = re.sub(r'<[^>]+>', ' ', html)
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # Identificar posibles bloques de partidos
    lines = clean_text.split(' São Paulo ')

    count = 1
    for i in range(1, len(lines)):
        fragment = lines[i][:200]  # Tomamos el fragmento alrededor de la mención
        if ' vs ' in fragment.lower() or ' - ' in fragment or ' VS ' in fragment:
            match_title = f'Partido/Resultado detectado #{count}: São Paulo {fragment[:80]}...'
            matches.append({
                'title': match_title,
                'description': (
                    f'Información extraída de Google Partidos: São Paulo'
                    f' {fragment}'
                ),
                'guid': f'spfc-match-{datetime.now().strftime("%Y%m%d")}-{count}',
            })
            count += 1

    # Si no se desglosa en bloques, genera una entrada general del estado actual
    if not matches:
        matches.append({
            'title': (
                f'São Paulo FC - Google Partidos ('
                f'{datetime.now().strftime("%d/%m/%Y")})'
            ),
            'description': (
                'Accede a la tarjeta oficial de Google para ver los'
                ' marcadores en vivo y próximos encuentros.'
            ),
            'guid': f'spfc-google-{datetime.now().strftime("%Y%m%d")}',
        })

    return matches


if __name__ == '__main__':
    items = get_google_matches()
    xml_data = build_rss_xml(items)

    with open('feed.xml', 'wb') as f:
        f.write(xml_data)

    print('Feed generado correctamente desde Google Partidos.')
