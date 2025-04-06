from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, ArticuloForm
from .models import Autor, Articulo

def index(request):
    return render(request, 'myapp/index.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Autor.objects.create(
                usuario=user,
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                pais=form.cleaned_data['pais']
            )
            login(request, user)
            return redirect('lista_articulos')
    else:
        form = RegistroForm()
    return render(request, 'myapp/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('lista_articulos')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'myapp/lista_articulos.html', {'articulos': articulos})

def detalle_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    return render(request, 'myapp/detalle.html', {'articulo': articulo})

@login_required
def crear_articulo(request):
    autor = get_object_or_404(Autor, usuario=request.user)
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = autor
            articulo.save()
            return redirect('detalle_articulo', pk=articulo.pk)
    else:
        form = ArticuloForm()
    return render(request, 'myapp/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if articulo.autor.usuario != request.user:
        return redirect('detalle_articulo', pk=pk)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', pk=pk)
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'myapp/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
def borrar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if articulo.autor.usuario == request.user:
        articulo.delete()
    return redirect('lista_articulos')

def about_view(request):
    return render(request, 'myapp/about.html')