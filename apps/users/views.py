from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import StudentLoginForm

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a una página home tras el login exitoso
    else:
        form = StudentLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def student_logout(request):
    logout(request)
    return redirect('student_login')

def student_register(request):
    # Aquí puedes agregar la lógica para registrar estudiantes
    return render(request, 'users/register.html')
