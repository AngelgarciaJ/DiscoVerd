from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),  # Ruta para el login
    path('register/', views.student_register, name='student_register'),  # Ruta para el registro
    path('logout/', views.student_logout, name='student_logout'),  # Ruta para el logout
]
