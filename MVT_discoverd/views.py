'''


# from django.shortcuts import render


# # Create your views here.
# # from django.shortcuts import render

# def landing_estudiantes(request):
#     return render(request, 'landing_estudiantes.html')

# def landing_organizadores(request):
#     return render(request, 'landing_organizadores.html')

'''
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser
# from .models import CustomUser, Departamento
from django.db import IntegrityError  # Importar la excepción IntegrityError

# # para eventos - dasboard
# from django.shortcuts import render, get_object_or_404
# from .models import Evento


def landing_estudiantes(request):
    return render(request, 'estudiantes/landing.html')

def login_estudiantes(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'student':
            login(request, user)
            return redirect('dashboard_estudiantes')
        else:
            return render(request, 'estudiantes/login.html', {'error': 'Credenciales incorrectas o no es estudiante'})
    return render(request, 'estudiantes/login.html')



# pruba de registro, caso email duplicados... 

def registro_estudiantes(request):
    if request.method == 'POST':
        # Recogemos los datos del formulario
        nombre = request.POST['nombre']
        email = request.POST['email']
        password = request.POST['password']
        mayor_edad = request.POST.get('mayor_edad') == 'on'

        # Verificar que el usuario es mayor de edad
        if mayor_edad:
            try:
                # Verificamos si el email ya existe
                if CustomUser.objects.filter(email=email).exists():
                    return render(request, 'estudiantes/registro.html', {'error': 'Este correo electrónico ya está registrado.'})

                # Creamos el usuario con el modelo CustomUser
                user = CustomUser.objects.create_user(
                    username=nombre, password=password, email=email, role='student'
                )
                return redirect('perfilamiento_estudiantes')  # Redirigimos a la página de perfilamiento

            except IntegrityError:
                # Si ocurre algún error de integridad, lo manejamos
                return render(request, 'estudiantes/registro.html', {'error': 'Error al crear el usuario, intenta de nuevo.'})
        else:
            # Si el checkbox de mayor de edad no está marcado, mostramos un mensaje de error
            return render(request, 'estudiantes/registro.html', {'error': 'Debes ser mayor de edad para registrarte'})

    # Si es una solicitud GET, simplemente mostramos el formulario de registro
    return render(request, 'estudiantes/registro.html')



def perfilamiento_estudiantes(request):
    if request.method == 'POST':
        intereses = request.POST.getlist('intereses')
        nivel_estudio = request.POST['nivel_estudio']
        disponibilidad = request.POST.getlist('disponibilidad')
        modo_participacion = request.POST['modo_participacion']
        objetivos = request.POST['objetivos']
        ubicacion = request.POST['ubicacion']
        ha_asistido_eventos = request.POST.get('ha_asistido_eventos') == 'on'

        # Guardamos los datos en el perfil del usuario
        user = request.user
        user.intereses = intereses  # Se espera un campo ManyToMany o CharField con varios valores
        user.nivel_estudio = nivel_estudio
        user.disponibilidad = disponibilidad
        user.modo_participacion = modo_participacion
        user.objetivos = objetivos
        user.ubicacion = ubicacion
        user.ha_asistido_eventos = ha_asistido_eventos
        user.save()

        return redirect('dashboard_estudiantes')  # Redirigimos al dashboard del estudiante una vez completado

    return render(request, 'estudiantes/perfilamiento.html')


#-----

# def dashboard_estudiantes(request):
#     # Esta será la vista del dashboard una vez el estudiante esté logueado
#     return render(request, 'estudiantes/dashboard.html')

# modulo del dasboard del estudiante central --- 
def dashboard_estudiantes(request):
    # Obtener eventos inscritos y recomendados para el estudiante
    eventos_inscritos = request.user.eventos_inscritos.all()
    eventos_recomendados = Evento.objects.exclude(id__in=eventos_inscritos)

    return render(request, 'estudiantes/dashboard.html', {
        'eventos_inscritos': eventos_inscritos,
        'eventos_recomendados': eventos_recomendados,
    })

def evento_detalle(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'estudiantes/evento_detalle.html', {'evento': evento})

def perfil_estudiante(request):
    return render(request, 'estudiantes/perfil.html')
