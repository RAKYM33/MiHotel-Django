
# MiHotel

Proyecto de gestión de reservas de hotel desarrollado con Django
durante el Máster de Desarrollo Web Full Stack de Conquer Blocks.

## Descripción

MiHotel es una aplicación web que permite gestionar habitaciones,
reservas y disponibilidad de un hotel de forma sencilla.

La aplicación dispone de una parte pública para realizar reservas
y una zona privada para el personal del hotel.

## Funcionalidades

- Consulta de habitaciones disponibles.
- Búsqueda de disponibilidad por fechas.
- Creación de reservas.
- Edición y eliminación de reservas.
- Validación de fechas.
- Prevención de reservas solapadas.
- Protección de reservas a nivel de base de datos PostgreSQL.
- Búsqueda por cliente y número de habitación.
- Cálculo de noches e importe total.
- Calendario mensual de ocupación.
- Visualización de habitaciones libres, ocupadas y no disponibles.
- Navegación entre meses.
- Panel de administración.
- Control de acceso para el personal.
- Tests automatizados.

## Tecnologías utilizadas

- Python
- Django
- SQLite (desarrollo local)
- PostgreSQL (producción)
- Neon
- Render
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

Generar una clave secreta para una instalación nueva:

```bash
python -c "from django.core.management.utils import get_random_secret_key; from pathlib import Path; Path('.env').open('x').write('SECRET_KEY=\"' + get_random_secret_key() + '\"\n')"
```

Si ya existe un archivo .env, conservar su configuración.

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

## Rutas principales

- `/` - Página principal y creación de reservas.
- `/reservas/` - Gestión de reservas.
- `/calendario/` - Calendario de ocupación.
- `/admin/` - Panel de administración.

Desde el panel de administración se pueden crear las habitaciones
necesarias para comenzar a realizar reservas.

## Despliegue

La aplicación utiliza Render como plataforma de alojamiento
y Neon como servicio de base de datos PostgreSQL.

Las credenciales y claves secretas se gestionan mediante
variables de entorno y no se incluyen en el repositorio.

## Tests

Para ejecutar las pruebas automatizadas:

```bash
python manage.py test reservas -v 2
```

El proyecto cuenta con 18 pruebas automatizadas que comprueban:

- Creación de habitaciones y reservas.
- Validación de fechas.
- Cálculo de noches y precios.
- Prevención de reservas solapadas.
- Edición de reservas.
- Control de acceso.
- Seguridad del calendario.
- Protección de integridad en PostgreSQL.

En SQLite se ejecutan 17 pruebas y se omite la prueba
específica de PostgreSQL.

## Autor

Joaquim Juaneda Mascaró

Proyecto académico de Conquer Blocks.
