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

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    grado = models.CharField(max_length=20, choices=GRADO_CHOICES, blank=True, null=True)
    bachillerato_tipo = models.CharField(max_length=10, choices=BACH_TYPE_CHOICES, blank=True, null=True)
    bachillerato_anio = models.CharField(max_length=2, choices=BACH_ANIO_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.username
