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
    path('estudiantes/dashboard/', views.dashboard_estudiantes, name='dashboard_estudiantes'),
]
