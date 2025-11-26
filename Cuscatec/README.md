# Cuscatec

Proyecto Django (POC) — sitio web simple con un solo app `cusca`.

Resumen rápido
- Django 5.2 project (single app `cusca`).
- Base de datos: SQLite (`db.sqlite3` en la raíz) — desarrollo local.
- Virtualenv: `env/` (ya existe en el workspace).

Estructura clave
- `Cuscatec/` (project package)
  - `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
- `cusca/` (app)
  - `views.py`, `urls.py`, `models.py`, `templates/cusca/`
  - `templates/cusca/base.html` — plantilla base que incluye la navbar
  - `templates/cusca/base_navbar.html` — navbar reutilizable (logo, usuario, menú, logout)
  - `templates/cusca/inicio.html`, `index.html`, `login.html`, `register.html`
- `static/`
  - `css/style.css` — estilos globales
  - `images/logo.png`

Configuración y ejecución (Windows PowerShell)
1. Activar entorno virtual:

```powershell
& .\env\Scripts\Activate.ps1
```

2. Instalar dependencias (si hace falta):

```powershell
pip install -r Cuscatec/requirements.txt
```

3. Migraciones / crear DB:

```powershell
python Cuscatec/manage.py makemigrations
python Cuscatec/manage.py migrate
```

4. Ejecutar servidor de desarrollo:

```powershell
python Cuscatec/manage.py runserver
```

Rutas importantes
- `/` -> `index` (ver `cusca/urls.py`)
- `/login/` -> login view
- `/register/` -> register view
- `/inicio/` -> página principal after login
- `/logout/` -> vista `logout` que hace `auth_logout` y redirige a `login`

Notas de templates y navbar
- `base_navbar.html`: barra superior fija. Contiene un botón que muestra el nombre del usuario (`{{ user.get_full_name|default:user.username }}`) y un menú desplegable con "Perfil", "Configuración" y "Cerrar sesión".
- El cierre de sesión se hace mediante un formulario oculto POST a la URL `logout` (CSRF incluido). La función JS global `logout()` somete ese formulario.
- `base.html` incluye la navbar, define bloques y ajusta el layout para que el footer quede al fondo.
- Los estilos del navbar y el script están, por ahora, inline en `base_navbar.html`. Se recomienda moverlos a `static/css/style.css` en una próxima iteración.

Dependencias backend
- Revisar `Cuscatec/requirements.txt` para ver las dependencias (Django 5.2.6, asgiref, sqlparse, tzdata).

Frontend
- No usa frameworks externos (Bootstrap/Tailwind/jQuery/React). Todo es HTML/CSS/vanilla JS.

Extensiones y recomendaciones (RAG / LangChain)
- Si quieres integrar LangChain/embeddings y RAG, sugiero usar Chroma o Qdrant como vector DB y OpenAI embeddings o sentence-transformers.
- Añadir dependencias ejemplo en `requirements.txt`: `langchain`, `openai`, `chromadb`, `tiktoken`.
- No almacenes claves en el repo — usa variables de entorno (`OPENAI_API_KEY`).

Cambios aplicados por el asistente
- Creó `cusca/templates/cusca/base_navbar.html`, `cusca/templates/cusca/base.html`.
- Migró `inicio.html` para extender `base.html` y centró su mensaje informativo.
- Ajustó footer para que quede al final de la página y sea ancho completo.
- Añadió comentarios en templates y creado `.github/CHANGES.md` con resumen.

Pruebas rápidas
- Iniciar servidor y verificar: navegación, menú de usuario (desplegable), logout (redirige a `/login/`).

Cómo contribuir
- Mantén estilos en `static/css/style.css` y evita inline styles.
- Añade nuevas rutas en `cusca/urls.py` y sus correspondientes vistas.

Si quieres, puedo:
- Mover estilos inline a `static/css/style.css` y limpiar templates (recomendado).
- Añadir un management command `ingest_docs` y módulos `vector_store.py` para un POC de RAG.

Contacto
- Repo: local workspace. Pide cualquier cambio y lo aplico.
