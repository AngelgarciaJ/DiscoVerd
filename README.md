# Plataforma de Gestión de Eventos
Un sistema para gestionar y participar en eventos de manera eficiente, diseñado para organizadores y estudiantes. Incluye scraping automatizado de datos desde fuentes externas.

## Índice
1. [Descripción](#descripción)
2. [Características](#características)
3. [Cómo Correr el Proyecto](#instalación)
4. [Uso](#uso)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Contribuciones](#contribuciones)
7. [Licencia](#licencia)


## Características
- Registro e inicio de sesión para usuarios y organizadores.
- Creación, edición, visualización y eliminación de eventos.
- Scraping automático de datos desde fuentes externas.
- Inscripción y cancelación de inscripción en eventos.
- Panel de administración para organizadores.

## Tecnologías Usadas
- Python 3.9 o superior
- pip
- Git
- Django
- SQLite
- BeautifulSoup (para scraping)
- Requests (para realizar solicitudes HTTP)
- HTML/CSS (para la interfaz de usuario)
- Entorno virtual (opcional, recomendado)


## Cómo Correr el Proyecto
1. Clona el repositorio:
   ```bash
   git clone https://github.com/AngelgarciaJ/DiscoVerd.git
   cd tu-repositorio
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---


## Uso
1. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
2. Abre tu navegador y ve a: `http://localhost:8000`.
3. Regístrate como organizador o usuario para empezar a crear o inscribirte en eventos.


## Estructura del Proyecto
```bash
📁MVT_discoverd
├── 📁scraping          # Módulo para realizar scraping web.
│   ├── scraper_eventos.py
├── 📁static            # Archivos estáticos (CSS, JS, imágenes).
│   ├── 📁css
│   ├── 📁img
│   ├── 📁js
├── 📁templates         # Plantillas HTML para la interfaz.
│   ├── 📁estudiantes
│   ├── 📁organizador
├── __init__.py         # Inicialización del paquete.
├── admin.py            # Configuración del administrador de Django.
├── apps.py             # Configuración de la aplicación.
├── models.py           # Modelos de base de datos.
├── tests.py            # Pruebas unitarias.
├── urls.py             # Rutas del proyecto.
└── views.py            # Lógica de vistas.

```

## Contribuciones
¡Las contribuciones son bienvenidas! Sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una nueva rama:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Haz tus cambios y realiza commit:
   ```bash
   git commit -am 'Agrega nueva funcionalidad'
   ```
4. Sube tus cambios a tu fork:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un Pull Request en el repositorio original.



## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](./LICENSE) para más detalles.
