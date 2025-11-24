from django.urls import path
from . import views 


urlpatterns = [
        path("", views.index, name="index"),
        path("login/", views.login, name="login"),
        path("register/", views.register, name="register"),
        path("inicio/", views.inicio, name="inicio"),
        path('logout/', views.logout, name='logout'),
        path("chat/", views.chat, name="chat"),



]

