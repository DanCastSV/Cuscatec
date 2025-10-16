# CHANGES

Resumen de cambios aplicados por el asistente:

- Se creó `cusca/templates/cusca/base_navbar.html`:
  - Barra de navegación reutilizable con logo/nombre de la app, botón de usuario y menú desplegable.
  - Función global `logout()` que somete un formulario oculto hacia `{% url 'logout' %}` (POST con CSRF).
  - Estilos y scripts incluidos inline para el POC.

- Se creó `cusca/templates/cusca/base.html`:
  - Plantilla base que incluye la navbar y define bloques `title`, `head`, `content` y `scripts`.
  - Layout en flex para que el footer quede al final de la página y ocupe todo el ancho.

- Se actualizó `cusca/templates/cusca/inicio.html`:
  - Ahora extiende `cusca/base.html` y coloca su contenido en `{% block content %}`.
  - El texto informativo fue centrado.

- Estilos y tamaño de la navbar ajustados (logo más grande, botón usuario más amplio) y el footer centrado.

Notas: Los enlaces "Perfil" y "Configuración" están como `#` porque no existían rutas detectadas para `profile` o `settings`. Se recomienda mover los estilos inline a `static/css/style.css` en una segunda iteración.
