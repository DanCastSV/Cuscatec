from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from django.shortcuts import render

def index(request):
    return render(request, "cusca/index.html")  # ruta dentro de templates/cusca


# Create your views here.
def login(request): 
     return render(request, "cusca/login.html")  # ruta dentro de templates/cusca

# Create your views here.
def register(request):
    return render(request, "cusca/register.html")  # ruta dentro de templates/cusca