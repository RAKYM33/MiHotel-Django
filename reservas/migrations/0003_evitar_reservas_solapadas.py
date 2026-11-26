from django.db import migrations


def crear_proteccion(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("""
            CREATE EXTENSION IF NOT EXISTS btree_gist;
        """)

        schema_editor.execute("""
            ALTER TABLE reservas_reserva
            ADD CONSTRAINT evitar_reservas_solapadas
            EXCLUDE USING gist (
                habitacion_id WITH =,
                daterange(fecha_entrada, fecha_salida, '[)') WITH &&
            );
        """)


def eliminar_proteccion(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("""
            ALTER TABLE reservas_reserva
            DROP CONSTRAINT IF EXISTS evitar_reservas_solapadas;
        """)


class Migration(migrations.Migration):

    dependencies = [
        ("reservas", "0002_reserva"),
    ]

    operations = [
        migrations.RunPython(
            crear_proteccion,
            eliminar_proteccion
        ),
    ]