from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


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
#############AQUI ESTABA EN OTRO MODELO


# Modelo para el perfil
class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    intereses = models.JSONField(default=list)
    nivel_estudio = models.CharField(max_length=50, default='')
    disponibilidad = models.JSONField(default=list)
    modo_participacion = models.CharField(max_length=20, default='presencial')
    objetivos = models.TextField(default='')
    ubicacion = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
#MODELO PARA EVENTOS
class Evento(models.Model):
    CATEGORIA_CHOICES = [
        ('academico', 'Académico'),
        ('cultural', 'Cultural'),
        ('deportivo', 'Deportivo'),
        ('tecnologia', 'Tecnología'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('finalizado', 'Finalizado')
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    hora_inicio = models.TimeField(
        default=datetime.time(9, 0)  # 9:00 AM por defecto
    )
    hora_fin = models.TimeField(
        default=datetime.time(18, 0)  # 6:00 PM por defecto
    )
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    ubicacion = models.CharField(
        max_length=200,
        default='Por determinar'
    )
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='academico'
    )
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='eventos_organizados',
    )
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='eventos_inscritos',
        through='Inscripcion'
    )
    cupo_maximo = models.IntegerField(default=100)
    contacto = models.CharField(
        max_length=100,
        default='Sin contacto especificado'
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente'
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    @property
    def plazas_disponibles(self):
        inscritos = self.participantes.count()
        return max(0, self.cupo_maximo - inscritos)

    class Meta:
        ordering = ['-fecha_creacion']
#class Evento(models.Model):
   # titulo = models.CharField(max_length=200)
   # imagen = models.ImageField(upload_to='eventos_imagenes/')
    #destacado = models.BooleanField(default=False)
    #fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    
class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    participante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    asistio = models.BooleanField(default=False)

    class Meta:
        unique_together = ['evento', 'participante']
        
### MODELO PARA EL ORGANIZADOR

class Organizador(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    facultad = models.CharField(max_length=100, null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)
    foto = models.ImageField(upload_to='organizadores/', null=True, blank=True)
    telefono_oficina = models.CharField(max_length=20, null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    ubicacion_oficina = models.CharField(max_length=100, null=True, blank=True)
    tipos_eventos = models.CharField(max_length=200, null=True, blank=True)
    preferencias_notificacion = models.CharField(max_length=20, default='all')
    perfil_completo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    