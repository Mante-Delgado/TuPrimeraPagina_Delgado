from django.shortcuts import render
from .models import Articulo

def index(request):
    return render(request, 'myapp/index.html')

def lista_articulos(request):
    articulos = Articulo.objects.all().order_by('-fecha_publicacion')
    return render(request, 'myapp/lista_articulos.html', {'articulos': articulos})