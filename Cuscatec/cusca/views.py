from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import RegistroForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PerfilUsuario
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import IntegrityError


def index(request):
    return render(request, "cusca/index.html")  # ruta dentro de templates/cusca


def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # El input se llama 'username' en el HTML
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('inicio')
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        except User.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
    return render(request, "cusca/login.html")  # ruta dentro de templates/cusca


def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            codigo = form.cleaned_data['codigo']
            telefono = form.cleaned_data['telefono']
            grado = form.cleaned_data.get('grado')
            bach_tipo = form.cleaned_data.get('bachillerato_tipo') or None
            bach_anio = form.cleaned_data.get('bachillerato_anio') or None
            password = form.cleaned_data['password']
            # la validación de confirm_password y reglas específicas ya las hace el form.clean()

            # comprobaciones básicas
            if User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya existe.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "El correo ya está registrado.")
            else:
                # si no es bachillerato, no guardar valores de bachillerato
                if grado != 'bachillerato':
                    bach_tipo = None
                    bach_anio = None
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    PerfilUsuario.objects.create(
                        user=user,
                        codigo=codigo,
                        telefono=telefono,
                        grado=grado,
                        bachillerato_tipo=bach_tipo,
                        bachillerato_anio=bach_anio
                    )
                    messages.success(request, "Usuario registrado correctamente.")
                    return redirect('login')
                except IntegrityError:
                    messages.error(request, "Error al crear el usuario. Intente nuevamente.")
        # si form no es válido, cae aquí y se re-renderiza con errores
    else:
        form = RegistroForm()
    return render(request, "cusca/register.html", {"form": form})  # ruta dentro de templates/cusca


def logout(request):
    auth_logout(request)
    return redirect('login')


def inicio(request):
    return render(request, "cusca/inicio.html")  # ruta dentro de templates/cusca

def chat(request):
    return render(request, "cusca/chat.html")