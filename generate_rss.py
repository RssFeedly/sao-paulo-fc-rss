import urllib.parse
import xml.etree.ElementTree as ET
import requests

# Búsqueda optimizada para resúmenes de partidos del São Paulo FC
QUERY = 'São Paulo FC "resumen" OR "melhores momentos" OR "partido"'
ENCODED_QUERY = urllib.parse.quote(QUERY)

# URL del feed de Google News para esa búsqueda en español/portugués
GOOGLE_NEWS_URL = f'https://news.google.com/rss/search?q={ENCODED_QUERY}&hl=pt-BR&gl=BR&ceid=BR:pt-150'


def fetch_and_filter_rss():
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
    }
    response = requests.get(GOOGLE_NEWS_URL, headers=headers)

    if response.status_code == 200:
        # Guardamos directamente el XML generado por Google adaptado
        with open('feed.xml', 'wb') as f:
            f.write(response.content)
        print('Feed RSS generado exitosamente en feed.xml')
    else:
        print(f'Error al obtener datos: {response.status_code}')


if __name__ == '__main__':
    fetch_and_filter_rss()
