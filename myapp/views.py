from django.shortcuts import render
from .models import Articulo

def index(request):
    return render(request, 'index.html')  
def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'lista_articulos.html', {'articulos': articulos})  