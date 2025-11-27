from django import forms
from django.core.exceptions import ValidationError
import os

GRADO_CHOICES = [
    ('kinder', 'Kínder'),
    ('preparatoria', 'Preparatoria'),
    ('1', 'Primero'),
    ('2', 'Segundo'),
    ('3', 'Tercero'),
    ('4', 'Cuarto'),
    ('5', 'Quinto'),
    ('6', 'Sexto'),
    ('7', 'Séptimo'),
    ('8', 'Octavo'),
    ('9', 'Noveno'),
    ('bachillerato', 'Bachillerato'),
]

MATERIA_CHOICES = [
    ('matematicas', 'Matemáticas'),
    ('lengua_literatura', 'Lengua y Literatura'),
    ('ciencias_sociales', 'Ciencias Sociales'),
    ('ingles', 'Inglés (Lengua Extranjera)'),
    ('educacion_fisica', 'Educación Física'),
    ('moral_urbanidad_civica', 'Moral, Urbanidad y Cívica / Ética y Ciudadana'),
    ('educacion_tecnologica', 'Educación Tecnológica / Informática'),
    ('historia', 'Historia'),
    ('orientacion_para_la_vida', 'Orientación para la Vida'),
    ('biologia', 'Biología'),
    ('fisica', 'Física'),
    ('quimica', 'Química'),
    ('filosofia', 'Filosofía'),
    ('gestion_empresarial', 'Gestión Empresarial'),
    ('servicio_social', 'Servicio Social'),
    ('teoria_del_conocimiento', 'Teoría del Conocimiento'),
]

BACH_TYPE_CHOICES = [
    ('general', 'General'),
    ('tecnico', 'Técnico Vocacional'),
]

BACH_ANIO_CHOICES = [
    ('1', '1° año'),
    ('2', '2° año'),
    ('3', '3° año'),
]

class RegistroForm(forms.Form):
    username = forms.CharField(
        label="Nombre completo",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre completo'
        })
    )

    email = forms.EmailField(
        label="Correo estudiantil",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo estudiantil'
        })
    )

    codigo = forms.CharField(
        label="Código de estudiante",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu código de estudiante'
        })
    )

    telefono = forms.RegexField(
        label="Número telefónico (con código de área)",
        regex=r'^\+\d{1,3}\s\d{4}\s\d{4}$',
        error_messages={'invalid': 'Formato inválido. Ejemplo: +503 1234 5678'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+503 1234 5678'
        })
    )

    grado = forms.ChoiceField(
        label="Grado",
        choices=GRADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    bachillerato_tipo = forms.ChoiceField(
        label="Tipo de Bachillerato",
        choices=BACH_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    bachillerato_anio = forms.ChoiceField(
        label="Año de Bachillerato",
        choices=BACH_ANIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )

    confirm_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        grado = cleaned_data.get("grado")
        bach_tipo = cleaned_data.get("bachillerato_tipo")
        bach_anio = cleaned_data.get("bachillerato_anio")

        # Validación de contraseñas
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden")

        # Validaciones específicas para bachillerato
        if grado == 'bachillerato':
            if not bach_tipo:
                self.add_error('bachillerato_tipo', "Seleccione el tipo de bachillerato (General o Técnico).")
            if not bach_anio:
                self.add_error('bachillerato_anio', "Seleccione el año de bachillerato.")
            if bach_tipo == 'general' and bach_anio == '3':
                self.add_error('bachillerato_anio', "Tercer año solo disponible para Bachillerato Técnico Vocacional.")
        else:
            # Si no es bachillerato, limpiar/ignorar campos relacionados para evitar problemas al guardar
            cleaned_data['bachillerato_tipo'] = ''
            cleaned_data['bachillerato_anio'] = ''

        return cleaned_data

class GuiaForm(forms.Form):
    titulo = forms.CharField(
        label="Título",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    grado = forms.ChoiceField(
        label="Grado",
        choices=GRADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    materia = forms.ChoiceField(
        label="Materia",
        choices=MATERIA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    archivo = forms.FileField(
        label="Archivo (PDF)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    def clean_archivo(self):
        f = self.cleaned_data.get('archivo')
        if not f:
            raise ValidationError("Debes subir un archivo PDF.")
        name = f.name.lower()
        if not name.endswith('.pdf'):
            raise ValidationError("El archivo debe ser un PDF.")
        max_mb = 10
        if f.size > max_mb * 1024 * 1024:
            raise ValidationError(f"El archivo no puede exceder {max_mb} MB.")
        return f
# Formulario para crear posts en el foro (ModelForm)
from .models import ForumPost


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del post'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }
