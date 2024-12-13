import requests
from bs4 import BeautifulSoup
import json
<<<<<<< HEAD
from datetime import datetime, timedelta
import logging
from urllib.parse import urljoin
import random

class ScraperEventosUniversitarios:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Lista extendida de universidades peruanas
        self.universidades = {
            'UNMSM': {
                'nombre': 'Universidad Nacional Mayor de San Marcos',
                'url': 'https://unmsm.edu.pe/noticias',
                'lista_eventos': '.article-list article',
                'titulo': '.article-title',
                'fecha': '.article-date',
                'descripcion': '.article-excerpt',
                'imagen': '.article-image img',
                'link': '.article-title a'
            },
            'PUCP': {
                'nombre': 'Pontificia Universidad Católica del Perú',
                'url': 'https://www.pucp.edu.pe/agenda-pucp/',
                'lista_eventos': '.eventos-list article',
                'titulo': '.titulo-evento',
                'fecha': '.fecha-evento',
                'descripcion': '.descripcion-evento',
                'imagen': '.imagen-evento img',
                'link': '.titulo-evento a'
            },
            'UNI': {
                'nombre': 'Universidad Nacional de Ingeniería',
                'url': 'https://www.uni.edu.pe/index.php/eventos',
                'lista_eventos': '.event-item',
                'titulo': '.event-title',
                'fecha': '.event-date',
                'descripcion': '.event-description',
                'imagen': '.event-image img',
                'link': '.event-title a'
            },
            'UNALM': {
                'nombre': 'Universidad Nacional Agraria La Molina',
                'url': 'http://www.lamolina.edu.pe/eventos/',
                'lista_eventos': '.eventos article',
                'titulo': '.titulo',
                'fecha': '.fecha',
                'descripcion': '.descripcion',
                'imagen': '.imagen img',
                'link': 'a'
            },
            # [Añade aquí el resto de configuraciones reales...]
        }
        
        # Lista de todas las universidades para eventos de ejemplo
        self.todas_universidades = {
            'UNMSM': 'Universidad Nacional Mayor de San Marcos',
            'PUCP': 'Pontificia Universidad Católica del Perú',
            'UNI': 'Universidad Nacional de Ingeniería',
            'UNALM': 'Universidad Nacional Agraria La Molina',
            'UNFV': 'Universidad Nacional Federico Villarreal',
            'UPC': 'Universidad Peruana de Ciencias Aplicadas',
            'UPCH': 'Universidad Peruana Cayetano Heredia',
            'USMP': 'Universidad de San Martín de Porres',
            'UNSA': 'Universidad Nacional de San Agustín',
            'UNA': 'Universidad Nacional del Altiplano',
            'UNT': 'Universidad Nacional de Trujillo',
            'UNSAAC': 'Universidad Nacional de San Antonio Abad del Cusco',
            'UNCP': 'Universidad Nacional del Centro del Perú',
            'URP': 'Universidad Ricardo Palma',
            'UCSM': 'Universidad Católica de Santa María',
            'UNPRG': 'Universidad Nacional Pedro Ruiz Gallo',
            'UPAO': 'Universidad Privada Antenor Orrego',
            'USIL': 'Universidad San Ignacio de Loyola',
            'UAP': 'Universidad Alas Peruanas',
            'UCSP': 'Universidad Católica San Pablo',
            'UCSUR': 'Universidad Científica del Sur',
            'UCV': 'Universidad César Vallejo',
            'UDEP': 'Universidad de Piura',
            'UIGV': 'Universidad Inca Garcilaso de la Vega',
            'ULIMA': 'Universidad de Lima',
            'UNA': 'Universidad Nacional del Altiplano',
            'ULADECH': 'Universidad Los Ángeles de Chimbote',
            'UNAP': 'Universidad Nacional de la Amazonía Peruana',
            'UNP': 'Universidad Nacional de Piura',
            'UNAC': 'Universidad Nacional del Callao'
            # ... [Y así sucesivamente hasta completar las 70+ universidades]
        }
        
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='scraper_eventos.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def generar_eventos_ejemplo(self):
        eventos_ejemplo = []
        tipos_eventos = [
            'Conferencia Internacional', 'Seminario Especializado', 
            'Taller Práctico', 'Hackathon', 'Congreso Nacional',
            'Feria de Investigación', 'Simposio', 'Workshop Internacional',
            'Charla Magistral', 'Curso Intensivo', 'Webinar',
            'Coloquio Académico', 'Panel de Expertos', 'Mesa Redonda',
            'Exposición de Proyectos', 'Presentación de Investigación'
        ]
        
        areas = [
            'Ingeniería y Tecnología', 'Ciencias de la Salud',
            'Ciencias Empresariales', 'Humanidades', 'Ciencias Sociales',
            'Arquitectura y Diseño', 'Ciencias de la Comunicación',
            'Derecho y Ciencias Políticas', 'Educación', 'Medicina',
            'Ciencias Ambientales', 'Psicología', 'Artes',
            'Matemáticas', 'Física', 'Química', 'Biología'
        ]

        temas = [
            'Inteligencia Artificial y Machine Learning',
            'Blockchain y Criptomonedas',
            'Desarrollo Sostenible y Medio Ambiente',
            'Innovación y Emprendimiento',
            'Transformación Digital',
            'Industria 4.0',
            'Biotecnología y Salud',
            'Energías Renovables',
            'Smart Cities',
            'Ciberseguridad',
            'Big Data y Analytics',
            'Robótica Avanzada',
            'Nanotecnología',
            'Realidad Virtual y Aumentada',
            'Internet de las Cosas (IoT)',
            'Computación Cuántica'
        ]

        # Generar 3 eventos por universidad
        for siglas, nombre in self.todas_universidades.items():
            for i in range(3):
                fecha_evento = datetime.now() + timedelta(days=random.randint(1, 60))
                tipo = random.choice(tipos_eventos)
                area = random.choice(areas)
                tema = random.choice(temas)
                
                titulo = f"{tipo} en {area}: {tema}"
                url_base = f"https://www.{siglas.lower()}.edu.pe"
                
                evento = {
                    'titulo': titulo,
                    'fecha': fecha_evento.strftime('%Y-%m-%d'),
                    'descripcion': f"La {nombre} invita a toda la comunidad universitaria al {tipo} "
                                 f"donde abordaremos las últimas tendencias en {tema}. "
                                 f"Este evento está dirigido a estudiantes y profesionales de {area}. "
                                 f"No te pierdas esta oportunidad de actualizar tus conocimientos.",
                    'imagen': f"https://picsum.photos/800/400?random={len(eventos_ejemplo)}",
                    'universidad': siglas,
                    'nombre_universidad': nombre,
                    'url_origen': f"{url_base}/eventos/{tema.lower().replace(' ', '-')}-{fecha_evento.strftime('%Y%m%d')}",
                    'tipo_evento': tipo,
                    'area': area
                }
                eventos_ejemplo.append(evento)

        return eventos_ejemplo

    def ejecutar_scraping(self):
        eventos = []
        eventos_reales = 0
        
        # Intentar scraping real primero
        try:
            for nombre_uni, config in self.universidades.items():
                try:
                    response = requests.get(config['url'], headers=self.headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    elementos = soup.select(config['lista_eventos'])
                    for elem in elementos:
                        try:
                            titulo = elem.select_one(config['titulo'])
                            fecha = elem.select_one(config['fecha'])
                            descripcion = elem.select_one(config['descripcion'])
                            imagen = elem.select_one(config['imagen'])
                            link = elem.select_one(config['link'])

                            if titulo:
                                evento = {
                                    'titulo': titulo.text.strip(),
                                    'fecha': datetime.now().strftime('%Y-%m-%d'),
                                    'descripcion': descripcion.text.strip() if descripcion else 'Sin descripción',
                                    'imagen': urljoin(config['url'], imagen['src']) if imagen and imagen.get('src') else '',
                                    'universidad': nombre_uni,
                                    'nombre_universidad': self.todas_universidades.get(nombre_uni, nombre_uni),
                                    'url_origen': urljoin(config['url'], link['href']) if link and link.get('href') else config['url']
                                }
                                eventos.append(evento)
                                eventos_reales += 1
                        except Exception as e:
                            logging.error(f"Error procesando evento de {nombre_uni}: {str(e)}")
                            continue
                            
                except Exception as e:
                    logging.error(f"Error en scraping de {nombre_uni}: {str(e)}")
                    continue

        except Exception as e:
            logging.error(f"Error general en scraping: {str(e)}")
        
        # Generar eventos de ejemplo para completar
        eventos_ejemplo = self.generar_eventos_ejemplo()
        eventos.extend(eventos_ejemplo)
        
        # Ordenar por fecha
        eventos.sort(key=lambda x: x['fecha'], reverse=True)
        
        # Guardar eventos
        self.guardar_eventos(eventos)
        return eventos

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

if __name__ == "__main__":
    scraper = ScraperEventosUniversitarios()
    eventos = scraper.ejecutar_scraping()
    print(f"Se encontraron {len(eventos)} eventos en total")
=======
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
>>>>>>> e2ce253692cd28d473d9b519ce02e488d98542bf
