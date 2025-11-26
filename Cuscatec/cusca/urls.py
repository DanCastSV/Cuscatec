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
]

