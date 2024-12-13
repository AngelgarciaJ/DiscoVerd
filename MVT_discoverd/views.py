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
## ESTA AQUI POR SI ACASO
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
### ESTOY AGREGANDO

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
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        try:
            # Actualizar campos básicos
            perfil.nombre_completo = request.POST.get('nombre_completo')
            perfil.telefono = request.POST.get('telefono')
            perfil.departamento = request.POST.get('departamento')
            perfil.distrito = request.POST.get('distrito')
            
            # Actualizar campos académicos
            perfil.universidad = request.POST.get('universidad')
            perfil.facultad = request.POST.get('facultad')
            perfil.ciclo_actual = request.POST.get('ciclo')
            
            # Actualizar preferencias
            perfil.modalidad_preferida = request.POST.get('modalidad')
            perfil.horarios_disponibles = request.POST.getlist('horarios[]')
            perfil.distancia_maxima = request.POST.get('distancia_maxima')
            
            # Verificar si todos los campos requeridos están completos
            campos_requeridos = [
                perfil.nombre_completo,
                perfil.telefono,
                perfil.departamento,
                perfil.distrito,
                perfil.universidad,
                perfil.facultad,
                perfil.ciclo_actual,
                perfil.modalidad_preferida,
                perfil.horarios_disponibles
            ]
            
            if all(campos_requeridos):
                perfil.perfilamiento_completado = True
                perfil.save()
                return redirect('completar_perfil')
            else:
                messages.error(request, "Por favor complete todos los campos requeridos")
                
        except Exception as e:
            messages.error(request, f'Error al guardar el perfil: {str(e)}')
    
    return render(request, 'estudiantes/perfilamiento.html', {'perfil': perfil})


def __str__(self):
        return f"Perfil de {self.nombre_completo}"
    
def save(self, *args, **kwargs):
        # Marcar el perfil como completado si todos los campos requeridos están llenos
        if all([
            self.nombre_completo,
            self.telefono,
            self.departamento,
            self.distrito,
            self.universidad,
            self.facultad,
            self.ciclo_actual,
            self.modalidad_preferida,
            self.horarios_disponibles
        ]):
            self.perfil_completado = True
        super().save(*args, **kwargs)


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
    try:
        # Imprimir para debugging
        perfil = Perfil.objects.get(usuario=request.user)
        print("Perfil encontrado:", perfil)
        print("Foto URL:", perfil.foto.url if perfil.foto else "No hay foto")
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(usuario=request.user)
        print("Nuevo perfil creado")
    # Instancia del scraper
    scraper = ScraperEventosUniversitarios()

    # Ejecuta el scraping para obtener eventos
    eventos = scraper.ejecutar_scraping()
    
    # Obtener eventos de organizadores
    eventos_organizador = Evento.objects.filter(
        estado='aprobado',
        activo=True,
        fecha__gte=timezone.now()
    ).select_related('organizador').order_by('fecha')##  aumente aqui 
    # Para debugging
    print("Debug - Total eventos:", eventos_organizador.count())
    for e in eventos_organizador:
        print(f"Debug - {e.titulo}: estado={e.estado}, activo={e.activo}, fecha={e.fecha}")
    # Contexto para la plantilla
    context = {
        'perfil': perfil,  # Añadir el perfil al contexto
        'eventos': eventos,
        'eventos_organizador': eventos_organizador,  # Añadir esto al contexto
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
        'es_creador': evento.organizador == request.user
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
        # Mantener el email en el formulario 
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
                return render(request, 'organizador/login_orga.html', {
                    'error_message': "Esta cuenta no tiene permisos de organizador",
                    'email': email
                })
                # Si las credenciales son incorrectas
        return render(request, 'organizador/login_orga.html', {
            'error_message': "Correo o contraseña incorrectos",
            'email': email
        })
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
    try:
        organizador = request.user.organizador
    except Organizador.DoesNotExist:
        messages.error(request, "No tiene permisos de organizador")
        return redirect('login_organizador')

    if organizador.perfil_completo:
        return redirect('landing_organizador')

    if request.method == 'POST':
        try:
            # Validaciones de campos
            facultad = request.POST.get('facultad')
            cargo = request.POST.get('cargo')
            biografia = request.POST.get('biografia')
            telefono_oficina = request.POST.get('telefono_oficina')
            ubicacion_oficina = request.POST.get('ubicacion_oficina')

            # Validación de campos requeridos
            if not facultad:
                messages.warning(request, "Por favor seleccione una facultad")
                return render(request, 'organizador/completPerfil_orga.html', {'organizador': organizador})
            
            if not cargo:
                messages.warning(request, "Por favor seleccione un cargo")
                return render(request, 'organizador/completPerfil_orga.html', {'organizador': organizador})

            # Validación de la foto
            if 'foto' in request.FILES:
                foto = request.FILES['foto']
                if foto.size > 1024 * 1024:  # 1MB
                    messages.warning(request, "La imagen debe ser menor a 1MB")
                    return render(request, 'organizador/completPerfil_orga.html', {'organizador': organizador})

                allowed_types = ['image/jpeg', 'image/png', 'image/gif']
                if foto.content_type not in allowed_types:
                    messages.warning(request, "Por favor suba una imagen en formato JPG, PNG o GIF")
                    return render(request, 'organizador/completPerfil_orga.html', {'organizador': organizador})

                organizador.foto = foto

            # Validación del teléfono
            if telefono_oficina and not telefono_oficina.isdigit():
                messages.warning(request, "El teléfono debe contener solo números")
                return render(request, 'organizador/completPerfil_orga.html', {'organizador': organizador})

            # Actualizar datos del perfil
            organizador.facultad = facultad
            organizador.cargo = cargo
            organizador.biografia = biografia
            organizador.telefono_oficina = telefono_oficina
            organizador.extension = request.POST.get('extension')
            organizador.ubicacion_oficina = ubicacion_oficina
            
            # Manejar tipos de eventos
            tipos_eventos = request.POST.getlist('tipos_eventos[]')
            if not tipos_eventos:
                messages.warning(request, "Por favor seleccione al menos un tipo de evento")
                return render(request, 'organizador/completPerfil_orga.html', {'organizador': organizador})
                
            organizador.tipos_eventos = ','.join(tipos_eventos)
            organizador.preferencias_notificacion = request.POST.get('preferencias_notificacion')
            organizador.perfil_completo = True
            organizador.save()
            
            messages.success(request, "Perfil completado exitosamente")
            return redirect('landing_organizador')
            
        except Exception as e:
            messages.error(request, "Ha ocurrido un error al actualizar el perfil. Por favor, intente nuevamente.")
            print(f"Error en completar_perfil_organizador: {str(e)}")  # Para debugging
            
    return render(request, 'organizador/completPerfil_orga.html', {
        'organizador': organizador
    })
    
@login_required
def landing_organizador(request):
    return render(request, 'organizador/LandingPage_orga.html', {
        'nombre_completo': f"{request.user.first_name} {request.user.last_name}"
    })
  ## aqui  hise algunos cambioas  
@login_required
def pagina_principal_organizador(request):
        # Obtener eventos del organizador actual
        proximos_eventos = Evento.objects.filter(
            organizador=request.user,
            fecha__gte=timezone.now()
        ).order_by('fecha')
        
        
        # Estadísticas
        total_eventos = Evento.objects.filter(organizador=request.user).count()
        eventos_activos = proximos_eventos.filter(estado='aprobado').count()
        total_participantes = sum(evento.participantes.count() for evento in proximos_eventos)
        pendientes_aprobacion = proximos_eventos.filter(estado='pendiente').count()
            
        context = {
            'nombre_completo': f"{request.user.first_name} {request.user.last_name}",
            'proximos_eventos': proximos_eventos,  # Cambié 'eventos' a 'proximos_eventos'
            'total_eventos': total_eventos,
            'eventos_activos': eventos_activos,
            'total_participantes': total_participantes,
            'pendientes_aprobacion': pendientes_aprobacion
        }
        
        return render(request, 'organizador/pagPrincipal_orga.html', context)
#para eventos, 
@login_required
def crear_evento(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            data = request.POST
            imagen = request.FILES.get('imagen')
            
            # Validar fecha y hora
            #fecha_str = f"{data.get('fecha')} {data.get('hora_inicio')}"
            #fecha_evento = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M')
            # Convertir fecha string a datetime
            # Combinar región y ubicación específica
            region = data.get('region', '')
            ubicacion_especifica = data.get('ubicacion_especifica', '')
            ubicacion_completa = f"{ubicacion_especifica}, {region}"
            
            fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d').date()
            
            # Crear el evento
            evento = Evento.objects.create(
                organizador=request.user,
                titulo=data.get('titulo'),
                descripcion=data.get('descripcion'),
                #fecha=fecha_evento,
                fecha=fecha,
                hora_inicio=data.get('hora_inicio'),
                hora_fin=data.get('hora_fin'),
                ubicacion=ubicacion_completa, 
                categoria=data.get('categoria'),
                cupo_maximo=data.get('cupo_maximo'),
                contacto=data.get('contacto'),
                estado='aprobado',  # O 'pendiente' si requiere aprobación
                activo=True
            )
            
            if imagen:
                #fs = FileSystemStorage()
                #filename = fs.save(f'eventos/{imagen.name}', imagen)
                #evento.imagen = filename
                evento.imagen = imagen
                evento.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Evento creado exitosamente',
                'evento_id': evento.id
            })
            
        except Exception as e:
            print(f"Error al crear evento: {str(e)}")
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
@csrf_exempt  # Solo para pruebas, en producción maneja el CSRF apropiadamente
@require_http_methods(["GET", "PUT", "DELETE"])
def evento_detail(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        
        if request.method == 'GET':
            # Convertir el evento a diccionario
            data = {
                'id': evento.id,
                'titulo': evento.titulo,
                'descripcion': evento.descripcion,
                'fecha': evento.fecha.strftime('%Y-%m-%d'),
                'hora_inicio': evento.hora_inicio.strftime('%H:%M'),
                'hora_fin': evento.hora_fin.strftime('%H:%M'),
                'ubicacion': evento.ubicacion,
                'categoria': evento.categoria,
                'cupo_maximo': evento.cupo_maximo,
                'contacto': evento.contacto,
                'estado': evento.estado,
                'imagen_url': evento.imagen.url if evento.imagen else None,
            }
            return JsonResponse(data)
        elif request.method == 'DELETE':
            evento.delete()
            return JsonResponse({'status': 'success', 'message': 'Evento eliminado correctamente'})
            
        elif request.method == 'PUT':
            data = json.loads(request.body)
            evento.titulo = data.get('titulo', evento.titulo)
            evento.descripcion = data.get('descripcion', evento.descripcion)
            evento.fecha = datetime.strptime(data.get('fecha', evento.fecha.strftime('%Y-%m-%d')), '%Y-%m-%d')
            evento.hora_inicio = datetime.strptime(data.get('hora_inicio', evento.hora_inicio.strftime('%H:%M')), '%H:%M').time()
            evento.hora_fin = datetime.strptime(data.get('hora_fin', evento.hora_fin.strftime('%H:%M')), '%H:%M').time()
            evento.ubicacion = data.get('ubicacion', evento.ubicacion)
            evento.categoria = data.get('categoria', evento.categoria)
            evento.cupo_maximo = data.get('cupo_maximo', evento.cupo_maximo)
            evento.contacto = data.get('contacto', evento.contacto)
            evento.save()
            return JsonResponse({'status': 'success'})
            
            
    except Evento.DoesNotExist:
        return JsonResponse({'error': 'Evento no encontrado'}, status=404)
   
@login_required
def mi_perfil_organizador(request):
    # Obtener perfil del usuario
    try:
        # Intenta obtener perfil de organizador
        organizador = Organizador.objects.get(user=request.user)
        context = {
            'nombre_completo': f"{organizador.nombres} {organizador.apellidos}",
            'perfil': organizador,
            'es_organizador': True
        }
    except Organizador.DoesNotExist:
        # Si no es organizador, obtener perfil de estudiante
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            context = {
                'nombre_completo': request.user.first_name,
                'perfil': perfil,
                'es_organizador': False
            }
        except Perfil.DoesNotExist:
            # Crear perfil básico si no existe
            perfil = Perfil.objects.create(usuario=request.user)
            context = {
                'nombre_completo': request.user.first_name,
                'perfil': perfil,
                'es_organizador': False
            }
    
    return render(request, 'organizador/mi_perfil_orga.html', context)

def about_events(request):
    return render(request, 'estudiantes/about_events.html')


def events(request):
    eventos_destacados = Evento.objects.filter(
        estado='aprobado',
        activo=True
    ).order_by('-fecha')[:6]  # Mostrar los 6 eventos más recientes
    
    return render(request, 'estudiantes/events.html', {
        'eventos_destacados': eventos_destacados
    })