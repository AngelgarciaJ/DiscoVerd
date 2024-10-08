
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Extendemos el modelo de usuario básico de Django
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Otros campos personalizados para tu modelo

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Cambia related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Cambia related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


# Modelo para organizar eventos (solo para organizadores)
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'organizer'})

    def __str__(self):
        return self.title
