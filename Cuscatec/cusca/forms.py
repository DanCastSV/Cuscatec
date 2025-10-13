from django import forms    

class RegistroForm(forms.Form):
    username = forms.CharField(
        label="Nombre completo",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # clase CSS para tu estilo
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

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden")