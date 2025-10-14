from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import RegistroForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PerfilUsuario
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def index(request):
    return render(request, "cusca/index.html")  # ruta dentro de templates/cusca


# Create your views here.
def login(request): 
    if request.method == 'POST':
        email = request.POST.get('username')  # El input se llama 'username' en el HTML
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('inicio')
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        except User.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
    return render(request, "cusca/login.html")  # ruta dentro de templates/cusca

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            codigo = form.cleaned_data['codigo']
            telefono = form.cleaned_data['telefono']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Las contraseñas no coinciden.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "El correo ya está registrado.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                PerfilUsuario.objects.create(user=user, codigo=codigo, telefono=telefono)
                messages.success(request, "Usuario registrado correctamente.")
                return redirect('login')
    else:
        form = RegistroForm()
    return render(request, "cusca/register.html", {"form": form})  # ruta dentro de templates/cusca

def logout(request):
    auth_logout(request)
    return redirect('login')

def inicio(request):
    return render(request, "cusca/inicio.html")  # ruta dentro de templates/cusca