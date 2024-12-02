from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views  # Añade esta línea
from . import views


urlpatterns = [
    
    # Landing page para estudiantes y autenticacion
    path('', views.landing_estudiantes, name='landing_estudiantes'),
    path('estudiantes/login/', views.login_estudiantes, name='login_estudiantes'),
    path('estudiantes/registro/', views.registro_estudiantes, name='registro_estudiantes'),
    #flujo de registro
    path('estudiantes/perfilamiento/', views.perfilamiento_estudiantes, name='perfilamiento_estudiantes'),
    path('estudiantes/completar-perfil/', views.completar_perfil, name='completar_perfil'),
   #paginasprincipales
    path('estudiantes/pantalla-principal/', views.pantalla_principal, name='pantalla_principal'),
    path('estudiantes/perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    path('mis-eventos/', views.mis_eventos, name='mis_eventos'),  # Nueva URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),#NUEVA URL
    #gestion de eventos
    path('eventos/<int:evento_id>/inscribir/', views.inscribir_evento, name='inscribir_evento'),
    path('eventos/<int:evento_id>/cancelar/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    #path('landing/', views.landing_page, name='landing_page'),
    
    path('perfil/', views.perfil, name='perfil'),
    
    ##esto es para el scrapingNUEVO##
    path('pantalla_principal/', views.pantalla_principal, name='pantalla_principal'),
    
    ### RUTAS PARA LOS ORGANIZADORES: 
    path('organizador/login/', views.login_organizador, name='login_organizador'),
    path('organizador/registro/', views.registro_organizador, name='registro_organizador'),
    path('organizador/completar-perfil/', views.completar_perfil_organizador, name='completar_perfil_organizador'),
    path('organizador/landing/', views.landing_organizador, name='landing_organizador'),
    path('organizador/panel/', views.pagina_principal_organizador, name='pagina_principal_organizador'),
    
    
    path('organizador/evento/crear/', views.crear_evento, name='crear_evento'),
    path('organizador/evento/<int:evento_id>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
    path('organizador/evento/<int:evento_id>/actualizar/', views.actualizar_evento, name='actualizar_evento'),
    path('eventos/<int:evento_id>/participantes/', views.detalles_evento, name='ver_participantes'),### AGREGE ESTO 
    path('eventos/<int:evento_id>/', views.detalles_evento, name='detalles_evento'),
]

# Para servir archivos multimedia en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# añadiendo la url para la Landin_page para el organizador
