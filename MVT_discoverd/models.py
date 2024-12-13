from django.db import models
# Extendemos el modelo de usuario básico de Django --
from django.contrib.auth.models import AbstractUser, Group, Permission, User

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, 
                            choices=[('student', 'Estudiante'), 
                                                    ('organizer', 'Organizador')], 
                            default='student')
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Cambia related_name
        blank=True,
        #help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Cambia related_name
        blank=True,
       # help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Nuevos campos para el perfilamiento
    intereses = models.TextField(null=True, blank=True)
    nivel_estudio = models.CharField(max_length=50, null=True, blank=True)
    disponibilidad = models.CharField(max_length=100, null=True, blank=True)
    modo_participacion = models.CharField(max_length=50, null=True, blank=True)
    objetivos = models.TextField(null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    ha_asistido_eventos = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

#     # evento - para ver de manera emergente -- pipi
# class Evento(models.Model):
#     nombre = models.CharField(max_length=200)
#     descripcion = models.TextField()
#     fecha = models.DateTimeField()
#     imagen = models.ImageField(upload_to='eventos/')
#     categoria = models.CharField(max_length=100)
#     estudiantes_inscritos = models.ManyToManyField(User, related_name="eventos_inscritos")

#     def __str__(self):
#         return self.nombre


# # Modelo para organizar eventos (solo para organizadores)
# class Event(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     date = models.DateTimeField()
#     organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'organizer'})

#     def __str__(self):
#         return self.title
