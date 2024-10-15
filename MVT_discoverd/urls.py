# from django.urls import path
# from . import views

# urlpatterns = [
#     path('estudiantes/', views.landing_estudiantes, name='landing_estudiantes'),
#     path('organizadores/', views.landing_organizadores, name='landing_organizadores'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('estudiantes/', views.landing_estudiantes, name='landing_estudiantes'),
    path('estudiantes/login/', views.login_estudiantes, name='login_estudiantes'),
    path('estudiantes/registro/', views.registro_estudiantes, name='registro_estudiantes'),
    path('estudiantes/perfilamiento/', views.perfilamiento_estudiantes, name='perfilamiento_estudiantes'),
    # path('estudiantes/dashboard/', views.dashboard_estudiantes, name='dashboard_estudiantes'),
    # # para dasboard
    # path('dashboard/', views.dashboard_estudiantes, name='dashboard_estudiante'),
    # path('eventos/<int:evento_id>/', views.evento_detalle, name='evento_detalle'),
    # path('perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    # # path('eventos_generales/', views.eventos_generales, name='eventos_generales'),
    # # path('estadisticas/', views.estadisticas_dashboard, name='estadisticas'),
]
