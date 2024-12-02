
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import CustomUser 
from django.db import IntegrityError
from .models import Perfil
from django.http import JsonResponse
from .models import Evento, Inscripcion

#ESTO ES PARA EL SCRAPING
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import json
import os
from datetime import datetime
from .scraping.scraper_eventos import ScraperEventosUniversitarios

### PARA EL ORGANIZADOR
from .models import Organizador
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.utils import timezone
from .models import Evento

User = get_user_model()  # Esto obtendrá tu modelo CustomUser

def landing_estudiantes(request):
    return render(request, 'estudiantes/landing.html')

def login_estudiantes(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticación por email y contraseña
        user = authenticate(request, email=email, password=password)
        if user and user.role == 'student':
            login(request, user)
            return redirect('pantalla_principal')  # Redirige al usuario a la página principal
        else:
            return render(request, 'estudiantes/login.html', {'error': 'Credenciales incorrectas'})
    
    return render(request, 'estudiantes/login.html')
           
def registro_estudiantes(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        password = request.POST['password']
        mayor_edad = request.POST.get('mayor_edad') == 'on'

        if mayor_edad:
            try:
                if CustomUser.objects.filter(email=email).exists():
                    return render(request, 'estudiantes/registro.html', 
                                {'error': 'Email ya registrado'})
                
                username = email.split('@')[0]
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=nombre,
                    role='student'
                )
                login(request, user)
                return redirect('perfilamiento_estudiantes')
            except Exception as e:
                print(f"Error: {str(e)}")  # Para debugging
                return render(request, 'estudiantes/registro.html', 
                            {'error': 'Error al crear usuario'})
        return render(request, 'estudiantes/registro.html', 
                     {'error': 'Debes ser mayor de edad'})
    return render(request, 'estudiantes/registro.html')
@login_required
def perfilamiento_estudiantes(request):
    if request.method == 'POST':
        try:
            # Obtener o crear el perfil
            perfil, created = Perfil.objects.get_or_create(usuario=request.user)
            
            # Guardar los datos del formulario
            perfil.intereses = request.POST.getlist('intereses')
            perfil.nivel_estudio = request.POST.get('nivel_estudio')
            perfil.disponibilidad = request.POST.getlist('disponibilidad')
            perfil.modo_participacion = request.POST.get('modo_participacion')
            perfil.objetivos = request.POST.get('objetivos')
            perfil.ubicacion = request.POST.get('ubicacion')
            perfil.save()
            
            print("Perfil guardado correctamente")  # Para debugging
            
            # Redireccionar
            return redirect('completar_perfil')
            
        except Exception as e:
            print(f"Error al guardar perfil: {e}")
            messages.error(request, "Error al guardar el perfil")
    context = {
        'intereses': [
            {'id': 1, 'nombre': 'Ciencia'},
            {'id': 2, 'nombre': 'Tecnología'},
            {'id': 3, 'nombre': 'Arte'},
            {'id': 4, 'nombre': 'Deportes'},
            {'id': 5, 'nombre': 'Emprendimiento'},
            {'id': 6, 'nombre': 'Voluntariado'}
        ]
    }
    return render(request, 'estudiantes/perfilamiento.html', context)

@login_required
def completar_perfil(request):
    perfil = Perfil.objects.get_or_create(usuario=request.user)[0]
    
    if request.method == 'POST':
        try:
            perfil.nombre_completo = request.POST.get('nombre_completo')
            perfil.carrera = request.POST.get('carrera')
            perfil.descripcion = request.POST.get('descripcion')
            if 'foto' in request.FILES:
                perfil.foto = request.FILES['foto']
            perfil.save()
            
            # Redirigir a pantalla principal después de completar perfil
            return redirect('pantalla_principal')
        except Exception as e:
            print(f"Error al completar perfil: {e}")
            messages.error(request, "Error al guardar los datos")
    
    return render(request, 'estudiantes/completar_perfil.html', {'perfil': perfil})
#@login_required
#def dashboard_estudiantes(request):
    #return render(request, 'estudiantes/dashboard.html')

@login_required
def perfil_estudiante(request):
    try:
        perfil = Perfil.objects.get(usuario=request.user)
        context = {
            'perfil': perfil
        }
        return render(request, 'estudiantes/perfil.html', context)
    except Perfil.DoesNotExist:
        messages.error(request, "No se encontró el perfil")
        return redirect('pantalla_principal')


@ensure_csrf_cookie
def pantalla_principal(request):
    # Instancia del scraper
    scraper = ScraperEventosUniversitarios()

    # Ejecuta el scraping para obtener eventos
    eventos = scraper.ejecutar_scraping()

    # Contexto para la plantilla
    context = {
        'eventos': eventos,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),  # Última actualización
    }

    return render(request, 'estudiantes/pantalla_principal.html', context)

# Vistas para las APIs (opcional, si las necesitas)
def featured_events(request):
    """API para eventos destacados"""
    return JsonResponse({'eventos': []})

def upcoming_events(request):
    """API para próximos eventos"""
    return JsonResponse({'eventos': []})

    
@login_required
def detalles_evento(request, evento_id):### AQUI CAMBI SOLO HACER control Z
    evento = get_object_or_404(Evento, id=evento_id)
    
    context = {
        'evento': evento,
        'esta_inscrito': request.user in evento.participantes.all(),
        'plazas_disponibles': evento.plazas_disponibles,
    }
    
    return render(request, 'estudiantes/detalles_eventos.html', context)

@login_required
def inscribir_evento(request, evento_id):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, id=evento_id)
        if evento.plazas_disponibles > 0:
            Inscripcion.objects.get_or_create(
                evento=evento,
                participante=request.user
            )
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})
@login_required
def cancelar_inscripcion(request, evento_id):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, id=evento_id)
        evento.participantes.remove(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def mis_eventos(request):
    eventos_inscritos = Evento.objects.filter(
        participantes=request.user
    ).order_by('fecha')
    return render(request, 'estudiantes/mis_eventos.html', {
        'eventos': eventos_inscritos
    })

#from django.urls import path
#from . import views

@login_required
def perfil(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, 'estudiantes/perfil.html', {'perfil': perfil})

### PARA ORGANIZADORES: 

def login_organizador(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autenticar usuario
        user = authenticate(username=email, password=password)
        
        if user is not None:
            try:
                # Verificar si es organizador
                organizador = Organizador.objects.get(user=user)
                login(request, user)
                
                # Redirigir según el estado del perfil
                if organizador.perfil_completo:
                    return redirect('landing_organizador')
                else:
                    return redirect('completar_perfil_organizador')
                    
            except Organizador.DoesNotExist:
                messages.error(request, "Esta cuenta no tiene permisos de organizador")
                return render(request, 'organizador/login_orga.html')
        else:
            messages.error(request, "Correo o contraseña incorrectos")
            return render(request, 'organizador/login_orga.html')
            
    return render(request, 'organizador/login_orga.html')
def registro_organizador(request):
    if request.method == 'POST':
        # Obtener el paso actual del formulario
        current_step = request.POST.get('step', '1')
        
        if current_step == '1':
            # Validar datos del paso 1
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            password = request.POST.get('password')
            password_confirmation = request.POST.get('password_confirmation')

            # Validaciones
            if not all([nombres, apellidos, email, telefono, password, password_confirmation]):
                messages.error(request, "Todos los campos son obligatorios")
                return render(request, 'organizador/registro_orga.html', {'step': '1'})

            if password != password_confirmation:
                messages.error(request, "Las contraseñas no coinciden")
                return render(request, 'organizador/registro_orga.html', {'step': '1'})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Este correo ya está registrado")
                return render(request, 'organizador/registro_orga.html', {'step': '1'})

            # Guardar datos en sesión
            request.session['registro_data'] = {
                'nombres': nombres,
                'apellidos': apellidos,
                'email': email,
                'telefono': telefono,
                'password': password
            }

            # Pasar al paso 2
            return render(request, 'organizador/registro_orga.html', {'step': '2'})

        elif current_step == '2':
            try:
                # Recuperar datos del paso 1
                registro_data = request.session.get('registro_data', {})
                facultad = request.POST.get('facultad')
                cargo = request.POST.get('cargo')
                
                if not all([facultad, cargo]):
                    messages.error(request, "Todos los campos son obligatorios")
                    return render(request, 'organizador/registro_orga.html', {'step': '2'})

                # Crear usuario
                user = User.objects.create_user(
                    username=registro_data['email'],
                    email=registro_data['email'],
                    password=registro_data['password'],
                    first_name=registro_data['nombres'],
                    last_name=registro_data['apellidos']
                )

                # Crear organizador
                organizador = Organizador.objects.create(
                    user=user,
                    nombres=registro_data['nombres'],
                    apellidos=registro_data['apellidos'],
                    telefono=registro_data['telefono'],
                    facultad=facultad,
                    cargo=cargo,
                    perfil_completo=False
                )

                # Limpiar datos de sesión
                if 'registro_data' in request.session:
                    del request.session['registro_data']

                # Iniciar sesión
                login(request, user)
                #messages.success(request, "Registro exitoso. Por favor complete su perfil")
                return redirect('completar_perfil_organizador')
            

            except Exception as e:
                print(f"Error en registro: {str(e)}")
                messages.error(request, "Error al crear la cuenta")
                return render(request, 'organizador/registro_orga.html', {'step': '1'})

    # Para peticiones GET, mostrar el primer paso
    return render(request, 'organizador/registro_orga.html', {'step': '1'})
@login_required
def completar_perfil_organizador(request):
    # Intentar obtener el organizador del usuario actual
    try:
        organizador = request.user.organizador
    except Organizador.DoesNotExist:
        messages.error(request, "No tiene permisos de organizador")
        return redirect('login_organizador')

    # Si el perfil ya está completo, redirigir al landing
    if organizador.perfil_completo:
        return redirect('landing_organizador')

    if request.method == 'POST':
        try:
            # Manejar la foto de perfil
            if 'foto' in request.FILES:
                organizador.foto = request.FILES['foto']

            # Actualizar datos del perfil
            organizador.facultad = request.POST.get('facultad')
            organizador.cargo = request.POST.get('cargo')
            organizador.biografia = request.POST.get('biografia')
            organizador.telefono_oficina = request.POST.get('telefono_oficina')
            organizador.extension = request.POST.get('extension')
            organizador.ubicacion_oficina = request.POST.get('ubicacion_oficina')
            
            # Manejar tipos de eventos
            tipos_eventos = request.POST.getlist('tipos_eventos[]')
            organizador.tipos_eventos = ','.join(tipos_eventos) if tipos_eventos else ''
            
            organizador.preferencias_notificacion = request.POST.get('preferencias_notificacion')
            organizador.perfil_completo = True
            organizador.save()
            
            messages.success(request, "Perfil completado exitosamente")
            return redirect('landing_organizador')
            
        except Exception as e:
            messages.error(request, f"Error al actualizar el perfil: {str(e)}")
    
    # Para GET request, mostrar el formulario
    return render(request, 'organizador/completPerfil_orga.html', {
        'organizador': organizador
    })
    
    
@login_required
def landing_organizador(request):
    try:
        organizador = request.user.organizador
        if not organizador.perfil_completo:
            messages.info(request, "Por favor complete su perfil primero")
            return redirect('completar_perfil_organizador')

        return render(request, 'organizador/LandingPage_orga.html', {
            'organizador': organizador,
            'nombre_completo': f"{request.user.first_name} {request.user.last_name}"
        })
    except Organizador.DoesNotExist:
        messages.error(request, "No tiene permisos de organizador")
        return redirect('login_organizador')
  ## aqui  hise algunos cambioas  
@login_required
def pagina_principal_organizador(request):
    try:
        organizador = request.user.organizador
        if not organizador.perfil_completo:
            messages.warning(request, "Por favor complete su perfil primero")
            return redirect('completar_perfil_organizador')
        
        # Obtener eventos del organizador actual
        eventos = Evento.objects.filter(
            organizador=request.user,
            fecha__gte=timezone.now()
        ).order_by('fecha')
        
        
         # Estadísticas
        total_eventos = eventos.count()
        eventos_activos = eventos.filter(
            fecha__gte=timezone.now(),
            estado='aprobado'
        ).count()
        total_participantes = sum(evento.participantes.count() for evento in eventos)
        pendientes_aprobacion = eventos.filter(estado='pendiente').count()
            
        context = {
            'organizador': organizador,
            'nombre_completo': f"{request.user.first_name} {request.user.last_name}",
            'eventos': eventos,
            'total_eventos': total_eventos,
            'eventos_activos': eventos_activos,
            'total_participantes': total_participantes,
            'pendientes_aprobacion': pendientes_aprobacion
        }
        
        return render(request, 'organizador/pagPrincipal_orga.html', context)
    except Organizador.DoesNotExist:
        messages.error(request, "No tiene permisos de organizador")
        return redirect('login_organizador')
#para eventos, 
@login_required
def crear_evento(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            data = request.POST
            imagen = request.FILES.get('imagen')
            
            # Validar fecha y hora
            fecha_str = f"{data.get('fecha')} {data.get('hora_inicio')}"
            fecha_evento = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M')
            
            # Crear el evento
            evento = Evento.objects.create(
                organizador=request.user,
                titulo=data.get('titulo'),
                descripcion=data.get('descripcion'),
                fecha=fecha_evento,
                hora_inicio=data.get('hora_inicio'),
                hora_fin=data.get('hora_fin'),
                ubicacion=data.get('ubicacion'),
                categoria=data.get('categoria'),
                cupo_maximo=data.get('cupo_maximo'),
                contacto=data.get('contacto'),
                estado='aprobado',  # O 'pendiente' si requiere aprobación
                activo=True
            )
            
            if imagen:
                fs = FileSystemStorage()
                filename = fs.save(f'eventos/{imagen.name}', imagen)
                evento.imagen = filename
                evento.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Evento creado exitosamente',
                'evento_id': evento.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def eliminar_evento(request, evento_id):
    if request.method == 'POST':
        try:
            evento = get_object_or_404(Evento, id=evento_id, organizador=request.user)
            evento.delete()
            messages.success(request, "Evento eliminado exitosamente")
        except Exception as e:
            messages.error(request, f"Error al eliminar el evento: {str(e)}") 
    return redirect('pagina_principal_organizador')



@login_required
def actualizar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, organizador=request.user)
    
    if request.method == 'POST':
        try:
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha = request.POST.get('fecha')
            evento.hora_inicio = request.POST.get('hora_inicio')
            evento.hora_fin = request.POST.get('hora_fin')
            evento.ubicacion = request.POST.get('ubicacion')
            evento.categoria = request.POST.get('categoria')
            evento.cupo_maximo = request.POST.get('cupo_maximo')
            evento.contacto = request.POST.get('contacto')
            
            if request.FILES.get('imagen'):
                evento.imagen = request.FILES['imagen']
                
            evento.save()
            messages.success(request, "Evento actualizado exitosamente")
            return redirect('pagina_principal_organizador')
            
        except Exception as e:
            messages.error(request, f"Error al actualizar el evento: {str(e)}")
            
    return render(request, 'organizador/actualizar_evento.html', {'evento': evento})

