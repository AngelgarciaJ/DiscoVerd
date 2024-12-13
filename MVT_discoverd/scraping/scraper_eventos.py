import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import random

class ScraperEventosUniversitarios:
   def __init__(self):
       self.headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
       }
       self.urls = {
           'eventbrite': [
               'https://www.eventbrite.com.pe/d/peru/events/',
               'https://www.eventbrite.com.pe/e/de-lo-presencial-a-lo-remoto-disena-tu-primer-curso-virtual-gratis-tickets-1096132213959',
               'https://www.eventbrite.com.pe/e/lanzamiento-de-mi-negocio-tickets-1098128374529',
               'https://www.eventbrite.com.pe/e/entradas-innovaccion-779865397397',
           ],
           'joinnus': [
               'https://www.joinnus.com/events/festivales/arequipa-i-feria-internacional-del-caballo-65994',
               'https://www.joinnus.com/events/seminarios-conferencias/arequipa-6ta-rueda-de-negocios-65786',
               'https://www.joinnus.com/events/art-culture/arequipa-anii-afterlifedrumcode-66094'
               'https://www.enlima.pe/blog/critica-el-vicio-del-poder-de-adam-mckay'
               'https://www.enlima.pe/blog/la-transparencia-del-color'
           ],
           'otros': [
               'https://masmiro.com/es/visita-mas-miro/',
               'https://www.running4peru.com/eventos', 
               'https://www.redbull.com/es-es/events',
               'https://cayetano.edu.pe/eventos/',
               'https://utec.edu.pe/node/114'
               'https://www.enlima.pe/',
           ]
       }
       self.setup_logging()
       self.cached_eventos = []

   def setup_logging(self):
       logging.basicConfig(
           filename='scraper_eventos.log',
           level=logging.INFO,
           format='%(asctime)s - %(levelname)s - %(message)s'
       )

   def scrape_page(self, url, platform):
       try:
           response = requests.get(url, headers=self.headers, timeout=10)
           response.raise_for_status()
           soup = BeautifulSoup(response.text, 'html.parser')
           eventos = []

           # Selectores específicos por plataforma
           selectors = {
               'eventbrite': {
                   'img': 'picture img, .listing-hero__image, [class*="event-card"] img',
                   'title': 'h1[data-automation="listing-title"], [class*="event-card"] .eds-event-card__formatted-name--is-clamped',
                   'desc': '[data-automation="listing-description"], [class*="event-card"] .eds-event-card__formatted-description--is-clamped',
                   'date': '[data-automation="listing-date"], [class*="event-card"] .eds-event-card__formatted-date'
               },
               'joinnus': {
                   'img': '.event-image img, .event-hero img',
                   'title': '.event-title, h1.event-name',
                   'desc': '.event-description',
                   'date': '.event-date, .event-time'
               },
               'otros': {
                   'img': '[class*="banner"] img, [class*="hero"] img, [class*="main"] img',
                   'title': 'h1, [class*="title"]',
                   'desc': '[class*="description"], [class*="content"]',
                   'date': '[class*="date"], time'
               }
           }

           sel = selectors.get(platform, selectors['otros'])

           # Buscar eventos
           images = soup.select(sel['img'])
           titles = soup.select(sel['title'])
           descriptions = soup.select(sel['desc'])
           dates = soup.select(sel['date'])

           for i in range(min(len(images), len(titles))):
               if images[i].get('src'):
                   eventos.append({
                       'titulo': titles[i].text.strip(),
                       'imagen': images[i]['src'],
                       'url_origen': url,
                       'descripcion': descriptions[i].text.strip() if i < len(descriptions) else 'Sin descripción',
                       'fecha': dates[i].text.strip() if i < len(dates) else datetime.now().strftime('%Y-%m-%d'),
                       'plataforma': platform
                   })

           return eventos

       except Exception as e:
           logging.error(f"Error scraping {url}: {e}")
           return []

   def ejecutar_scraping(self):
       todos_eventos = []
       with ThreadPoolExecutor(max_workers=5) as executor:
           futures = []
           for platform, urls in self.urls.items():
               for url in urls:
                   futures.append(executor.submit(self.scrape_page, url, platform))

           for future in as_completed(futures):
               try:
                   eventos = future.result()
                   todos_eventos.extend(eventos)
               except Exception as e:
                   logging.error(f"Error en future: {e}")

       # Guardar todos los eventos encontrados en caché
       self.cached_eventos = todos_eventos
       
       # Seleccionar 20 eventos aleatorios
       if len(todos_eventos) > 20:
           eventos_seleccionados = random.sample(todos_eventos, 20)
       else:
           eventos_seleccionados = todos_eventos

       self.guardar_eventos(eventos_seleccionados)
       return eventos_seleccionados

   def guardar_eventos(self, eventos):
       try:
           data = {
               'ultima_actualizacion': datetime.now().isoformat(),
               'total_eventos': len(eventos),
               'eventos': eventos
           }
           
           with open('eventos.json', 'w', encoding='utf-8') as f:
               json.dump(data, f, ensure_ascii=False, indent=2)
           
           logging.info(f"Guardados {len(eventos)} eventos en eventos.json")
           
       except Exception as e:
           logging.error(f"Error guardando eventos: {str(e)}")

   def obtener_eventos_aleatorios(self, cantidad=20):
       if not self.cached_eventos:
           return self.ejecutar_scraping()
       
       return random.sample(
           self.cached_eventos, 
           min(cantidad, len(self.cached_eventos))
       )

if __name__ == "__main__":
   scraper = ScraperEventosUniversitarios()
   eventos = scraper.ejecutar_scraping()
   print(f"Se encontraron {len(eventos)} eventos en total")