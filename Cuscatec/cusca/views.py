from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from django.shortcuts import render

def index(request):
    return render(request, "cusca/index.html")  # ruta dentro de templates/cusca


# Create your views here.
