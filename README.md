
# MiHotel

Proyecto de gestión de reservas de hotel desarrollado con Django
durante el Máster de Desarrollo Web Full Stack de Conquer Blocks.

## Descripción

MiHotel es una aplicación web que permite gestionar habitaciones
y reservas de un hotel de forma sencilla.

## Funcionalidades

- Consulta de habitaciones disponibles.
- Búsqueda de disponibilidad por fechas.
- Creación de reservas.
- Edición y eliminación de reservas.
- Validación de fechas.
- Prevención de reservas solapadas.
- Búsqueda por cliente y número de habitación.
- Cálculo de noches e importe total.
- Panel de administración.
- Control de acceso para el personal.
- Tests automatizados.

## Tecnologías utilizadas

- Python
- Django
- SQLite
- HTML
- CSS
- Git y GitHub

## Instalación

Crear un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Generar una clave secreta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; from pathlib import Path; Path('.env').write_text('SECRET_KEY=\"' + get_random_secret_key() + '\"\n')"
```

Aplicar las migraciones:

```bash
python manage.py migrate
```

Crear un usuario administrador:

```bash
python manage.py createsuperuser
```

Iniciar el servidor:

```bash
python manage.py runserver
```

Acceder a la aplicación:

http://127.0.0.1:8000/

Desde el panel de administración se pueden crear las habitaciones
necesarias para comenzar a realizar reservas.

## Tests

Para ejecutar las pruebas automatizadas:

```bash
python manage.py test
```

El proyecto cuenta con 10 tests superados.

## Autor

Joaquim Juaneda Mascaró

Proyecto académico de Conquer Blocks.
