from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from .forms import RegistroForm, GuiaForm, ForumPostForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PerfilUsuario, Guia, ForumPost, StudentNews
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse  # agregado (opcional si quieres redirect a admin)
from django.core.paginator import Paginator

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


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def inicio(request):
    return render(request, "cusca/inicio.html")  # ruta dentro de templates/cusca

@login_required(login_url='login')
def chat(request):
    return render(request, "cusca/chat.html")

def super_login(request):
    """
    Inicio de sesión para superusuarios usando username (no email).
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                auth_login(request, user)
                return redirect('super_inicio')
            else:
                messages.error(request, "Acceso denegado: usuario no es superusuario.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    return render(request, "cusca/super_login.html")

# Nueva vista: panel/landing exclusivo para superusuarios
@login_required(login_url='super_login')
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def super_inicio(request):
    return render(request, "cusca/super_inicio.html")

@login_required(login_url='super_login')
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def subir_guia(request):
    """
    Vista para que superusuarios suban una guía (PDF) con título, grado y materia.
    """
    if request.method == 'POST':
        form = GuiaForm(request.POST, request.FILES)
        if form.is_valid():
            Guia.objects.create(
                titulo=form.cleaned_data['titulo'],
                grado=form.cleaned_data['grado'],
                materia=form.cleaned_data['materia'],
                archivo=form.cleaned_data['archivo'],
                uploaded_by=request.user
            )
            messages.success(request, "Guía subida correctamente.")
            return redirect('super_inicio')
    else:
        form = GuiaForm()
    return render(request, "cusca/super_subir_guia.html", {"form": form})

@login_required(login_url='super_login')
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def listar_guias_super(request):
    """
    Lista las guías agrupadas por materia. Muestra solo materias que tengan guías.
    """
    # obtener choices actuales del campo materia para etiquetas legibles
    materia_choices = dict(Guia._meta.get_field('materia').choices)
    # construir lista de (codigo, etiqueta, queryset)
    materias = []
    for codigo, etiqueta in materia_choices.items():
        qs = Guia.objects.filter(materia=codigo).order_by('-created_at')
        if qs.exists():
            materias.append({'codigo': codigo, 'etiqueta': etiqueta, 'guias': qs})
    return render(request, "cusca/super_guias_list.html", {"materias": materias})


@login_required(login_url='super_login')
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def guia_detalle(request, pk):
    """
    Vista para superusuarios: ver + eliminar (can_delete=True).
    """
    guia = get_object_or_404(Guia, pk=pk)
    return render(request, "cusca/guia_detalle.html", {"guia": guia, "can_delete": True})


@login_required(login_url='login')
def guia_detalle_public(request, pk):
    """
    Vista para usuarios normales: solo ver si el grado del usuario coincide con la guía.
    """
    guia = get_object_or_404(Guia, pk=pk)

    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        user_grado = perfil.grado
    except PerfilUsuario.DoesNotExist:
        user_grado = None

    if user_grado != guia.grado:
        messages.error(request, "No hay material disponible para tu grado.")
        return redirect('listar_guias')

    return render(request, "cusca/guia_detalle.html", {"guia": guia, "can_delete": False})

@login_required(login_url='super_login')
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def guia_eliminar(request, pk):
    """
    Elimina una guía (solo vía POST). Redirige a la lista con mensaje.
    """
    guia = get_object_or_404(Guia, pk=pk)

    if request.method != 'POST':
        return HttpResponseForbidden("Operación no permitida.")

    titulo = str(guia.titulo)
    guia.archivo.delete(save=False)  # borra archivo del storage
    guia.delete()
    messages.success(request, f"Guía «{titulo}» eliminada correctamente.")
    return redirect('listar_guias_super')

@login_required(login_url='login')
def listar_guias(request):
    """
    Lista para usuarios: muestra guías del grado del usuario agrupadas por materia.
    Si no hay guías muestra mensaje de 'no hay material disponible'.
    """
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        grado = perfil.grado
    except PerfilUsuario.DoesNotExist:
        grado = None

    materia_choices = dict(Guia._meta.get_field('materia').choices)
    materias = []

    if grado:
        for codigo, etiqueta in materia_choices.items():
            qs = Guia.objects.filter(materia=codigo, grado=grado).order_by('-created_at')
            if qs.exists():
                materias.append({'codigo': codigo, 'etiqueta': etiqueta, 'guias': qs})

    return render(request, "cusca/guias_list.html", {"materias": materias, "grado": grado})


# ===== VISTAS DEL FORO ===== 

@login_required(login_url='login')
def forum_list(request):
    """
    Lista de posts del foro con paginación (10 posts por página).
    Ordena por fecha de creación (más recientes primero).
    """
    posts = ForumPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cusca/forum_list.html', {'page_obj': page_obj})


@login_required(login_url='login')
def forum_detail(request, pk):
    """
    Detalle de un post del foro.
    """
    post = get_object_or_404(ForumPost, pk=pk)
    # Incrementar contador de vistas (opcional)
    post.views += 1
    post.save()
    return render(request, 'cusca/forum_detail.html', {'post': post})


@login_required(login_url='login')
def forum_create(request):
    """
    Crear un nuevo post en el foro.
    """
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Tu post fue creado exitosamente.')
            return redirect('forum_detail', pk=post.pk)
    else:
        form = ForumPostForm()
    return render(request, 'cusca/forum_form.html', {'form': form, 'action': 'crear'})


@login_required(login_url='login')
def forum_edit(request, pk):
    """
    Editar un post del foro (solo el autor o superusuario puede editar).
    """
    post = get_object_or_404(ForumPost, pk=pk)
    
    # Validar que solo el autor o un superusuario puedan editar
    if request.user != post.author and not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para editar este post.')
        return redirect('forum_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = ForumPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu post fue actualizado exitosamente.')
            return redirect('forum_detail', pk=post.pk)
    else:
        form = ForumPostForm(instance=post)
    return render(request, 'cusca/forum_form.html', {'form': form, 'action': 'editar', 'post': post})


@login_required(login_url='login')
def forum_delete(request, pk):
    """
    Eliminar un post del foro (solo el autor o superusuario puede eliminar).
    """
    post = get_object_or_404(ForumPost, pk=pk)
    
    # Validar que solo el autor o un superusuario puedan eliminar
    if request.user != post.author and not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para eliminar este post.')
        return redirect('forum_detail', pk=post.pk)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'El post "{post_title}" fue eliminado.')
        return redirect('forum_list')
    
    # GET: mostrar confirmación de eliminación
    return render(request, 'cusca/forum_confirm_delete.html', {'post': post})


# ===== VISTA DE NOTICIAS ESTUDIANTILES =====

@login_required(login_url='login')
def noticias_list(request):
    """
    Lista de noticias estudiantiles (solo activas).
    """
    noticias = StudentNews.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(noticias, 5)  # 5 noticias por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cusca/noticias_list.html', {'page_obj': page_obj})