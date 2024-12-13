from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
from django.urls import resolve
from django.shortcuts import redirect
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
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
    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('hibrido', 'Híbrido')
    ]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Información básica
    nombre_completo = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    departamento = models.CharField(max_length=50, null=True, blank=True)
    distrito = models.CharField(max_length=50, null=True, blank=True)
    
    # Información académica
    universidad = models.CharField(max_length=100, null=True, blank=True)
    facultad = models.CharField(max_length=100, null=True, blank=True)
    ciclo_actual = models.IntegerField(null=True, blank=True)
    
    # Preferencias
    modalidad_preferida = models.CharField(
        max_length=20,
        choices=MODALIDAD_CHOICES,
        default='presencial'
    )
    horarios_disponibles = models.JSONField(default=list)
    distancia_maxima = models.IntegerField(default=10)
    
    # Metadata
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    perfil_completado = models.BooleanField(default=False)
    
    foto = models.ImageField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        help_text='Foto de perfil del usuario'
    )

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def get_foto_url(self):
        if self.foto:
            return self.foto.url
        return None

    def save(self, *args, **kwargs):
        if self.foto:
            # Procesar la imagen antes de guardarla
            img = Image.open(self.foto)
            
            # Convertir a RGB si es necesario
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar si es muy grande
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
            
            # Guardar la imagen procesada
            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            self.foto = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{self.foto.name.split('.')[0]}.jpg",
                'image/jpeg',
                output.getbuffer().nbytes,
                None
            )
            
        super().save(*args, **kwargs)
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
        default='aprobado'
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
        
class PerfilamientoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # URLs que están exentas de la verificación
            exempt_urls = [
                'perfilamiento_estudiantes',
                'completar_perfil',
                'logout',
                'admin:index'
            ]
            
            current_url = resolve(request.path_info).url_name
            
            try:
                perfil = request.user.perfil
                # Si el usuario no ha completado el perfilamiento y no está en una URL exenta
                if not perfil.perfilamiento_completado and current_url not in exempt_urls:
                    return redirect('perfilamiento_estudiantes')
            except:
                # Si el usuario no tiene perfil, crear uno
                from MVT_discoverd.models import Perfil
                Perfil.objects.create(usuario=request.user)
                return redirect('perfilamiento_estudiantes')

        return self.get_response(request)
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

