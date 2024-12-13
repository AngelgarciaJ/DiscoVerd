import unittest
from unittest.mock import patch
from MVT_discoverd.scraping.scraper_eventos import ScraperEventosUniversitarios

class ScraperEventosTests(unittest.TestCase):

    @patch('MVT_discoverd.scraping.scraper_eventos.requests.get')
    def test_scraping_unmsm(self, mock_get):
        # Simular una respuesta HTTP
        mock_html = '''
        <html>
            <body>
                <div class="event">
                    <h2>Evento de Prueba</h2>
                    <p>Fecha: 2024-12-31</p>
                    <p>Ubicación: Lugar de Prueba</p>
                    <p>Descripción: Descripción del evento de prueba</p>
                </div>
            </body>
        </html>
        '''
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_html

        # Instanciar el scraper y ejecutar el scraping
        scraper = ScraperEventosUniversitarios()
        eventos = scraper.ejecutar_scraping()

        # Verificar que los datos obtenidos son los esperados
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]['nombre'], 'Evento de Prueba')
        self.assertEqual(eventos[0]['fecha'], '2024-12-31')
        self.assertEqual(eventos[0]['ubicacion'], 'Lugar de Prueba')
        self.assertEqual(eventos[0]['descripcion'], 'Descripción del evento de prueba')

if __name__ == '__main__':
    unittest.main()