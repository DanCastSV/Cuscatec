from django.db import models
from django.contrib.auth.models import User

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

MATERIA_CHOICES = [
    # Asignaturas comunes
    ('matematicas', 'Matemáticas'),
    ('lengua_literatura', 'Lengua y Literatura'),
    ('ciencias_sociales', 'Ciencias Sociales'),
    ('ingles', 'Inglés (Lengua Extranjera)'),
    ('educacion_fisica', 'Educación Física'),
    ('moral_urbanidad_civica', 'Moral, Urbanidad y Cívica / Ética y Ciudadana'),
    ('educacion_tecnologica', 'Educación Tecnológica / Informática'),
    # Asignaturas específicas del bachillerato general
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

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    grado = models.CharField(max_length=20, choices=GRADO_CHOICES, blank=True, null=True)
    bachillerato_tipo = models.CharField(max_length=10, choices=BACH_TYPE_CHOICES, blank=True, null=True)
    bachillerato_anio = models.CharField(max_length=2, choices=BACH_ANIO_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Nuevo: modelo para guías / PDFs
class Guia(models.Model):
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

    titulo = models.CharField(max_length=255)
    grado = models.CharField(max_length=32, choices=GRADO_CHOICES)
    materia = models.CharField(max_length=64, choices=MATERIA_CHOICES)  # nuevo campo
    archivo = models.FileField(upload_to='guias/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_grado_display()})"
