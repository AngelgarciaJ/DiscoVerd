# from django.shortcuts import render


# # Create your views here.
# # from django.shortcuts import render

# def landing_estudiantes(request):
#     return render(request, 'landing_estudiantes.html')

# def landing_organizadores(request):
#     return render(request, 'landing_organizadores.html')





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser

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

def registro_estudiantes(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = CustomUser.objects.create_user(username=username, password=password, email=email, role='student')
        return redirect('login_estudiantes')
    return render(request, 'estudiantes/registro.html')

def dashboard_estudiantes(request):
    # Esta será la vista del dashboard una vez el estudiante esté logueado
    return render(request, 'estudiantes/dashboard.html')
