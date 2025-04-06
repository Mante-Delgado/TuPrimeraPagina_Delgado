from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Articulo, Categoria

class RegistroForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(required=False)
    pais = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'fecha_nacimiento', 'pais']

class ArticuloForm(forms.ModelForm):
    categoria_nombre = forms.CharField(
        max_length=100,
        label="Categoría",
        widget=forms.TextInput(attrs={
            'list': 'lista_categorias',
            'placeholder': 'Ej: Dragones, Historia, etc.'
        }),
        help_text="Escribí una categoría existente o una nueva."
    )

    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'imagen']  