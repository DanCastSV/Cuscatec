from django import forms    

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

BACH_TYPE_CHOICES = [
    ('general', 'General'),
    ('tecnico', 'Técnico Vocacional'),
]

BACH_ANIO_CHOICES = [
    ('1', 'Primer año'),
    ('2', 'Segundo año'),
    ('3', 'Tercer año (solo Técnico)'),
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