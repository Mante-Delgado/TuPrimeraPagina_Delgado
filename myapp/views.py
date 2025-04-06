from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, ArticuloForm
from .models import Autor, Articulo, Categoria

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
            messages.success(request, f'¡Bienvenido {user.username}! Tu cuenta fue creada con éxito.')
            login(request, user)
            return redirect('lista_articulos')
    else:
        form = RegistroForm()
    return render(request, 'myapp/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        form.fields['username'].widget.attrs.update({'placeholder': 'Ingresá tu usuario'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Ingresá tu contraseña'})

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Sesión iniciada correctamente. ¡Hola, {user.username}!')
            return redirect('lista_articulos')
        else:
            messages.error(request, 'Usuario o contraseña inválidos. Intentá de nuevo.')
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({'placeholder': 'Ingresá tu usuario'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Ingresá tu contraseña'})

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
        form = ArticuloForm(request.POST, request.FILES)

        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = autor

            # Usamos el nuevo campo del formulario
            nombre_categoria = form.cleaned_data['categoria_nombre'].strip()
            categoria_obj, _ = Categoria.objects.get_or_create(nombre=nombre_categoria)
            articulo.categoria = categoria_obj

            articulo.save()
            messages.success(request, 'Artículo creado correctamente.')
            return redirect('detalle_articulo', pk=articulo.pk)

    else:
        form = ArticuloForm()

    return render(request, 'myapp/formulario.html', {
        'form': form,
        'accion': 'Crear',
        'categorias': Categoria.objects.all()
    })



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


