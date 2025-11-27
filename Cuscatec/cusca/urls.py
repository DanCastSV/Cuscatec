from django.urls import path
from . import views 


urlpatterns = [
        path("", views.index, name="index"),
        path("login/", views.login, name="login"),
        path("register/", views.register, name="register"),
        path("inicio/", views.inicio, name="inicio"),
        path('logout/', views.logout, name='logout'),
        path("chat/", views.chat, name="chat"),
        path('super-login/', views.super_login, name='super_login'),
        path('super-inicio/', views.super_inicio, name='super_inicio'),
        path('super/guias/subir/', views.subir_guia, name='subir_guia'),
        path('super/guias/', views.listar_guias_super, name='listar_guias_super'),
        path('super/guias/<int:pk>/', views.guia_detalle, name='guia_detalle'),
        path('super/guias/<int:pk>/eliminar/', views.guia_eliminar, name='guia_eliminar'),
        path('guias/', views.listar_guias, name='listar_guias'),
        path('guias/<int:pk>/', views.guia_detalle_public, name='guia_detalle_public'),
        # Rutas del foro
        path('foro/', views.forum_list, name='forum_list'),
        path('foro/<int:pk>/', views.forum_detail, name='forum_detail'),
        path('foro/nuevo/', views.forum_create, name='forum_create'),
        path('foro/<int:pk>/editar/', views.forum_edit, name='forum_edit'),
        path('foro/<int:pk>/eliminar/', views.forum_delete, name='forum_delete'),
        # Rutas de noticias
        path('noticias/', views.noticias_list, name='noticias_list'),
]

