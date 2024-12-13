from django.contrib import admin
from django.urls import path, include
#from MVT_discoverd import views as mvt_views

from django.conf import settings
from django.conf.urls.static import static
from MVT_discoverd import views  

urlpatterns = [
    # Administración de Django
    path('admin/', admin.site.urls),
    path('', views.landing_estudiantes, name='landing_estudiantes'), 
    
    path('', include('MVT_discoverd.urls')),
]

# Configuración para archivos multimedia en desarrollo

if settings.DEBUG:
    ### LO AUMENTE ESTO SINO FUNCIONA Es AQUI##
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

