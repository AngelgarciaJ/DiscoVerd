from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')  # Campos visibles
    search_fields = ('username', 'email')  # Barra de búsqueda
    list_filter = ('is_active', 'is_staff')  # Filtros laterales
    ordering = ('-date_joined',)  # Ordenar por fecha de creación descendente

