from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import connection, IntegrityError, transaction
from unittest import skipUnless
from datetime import date
from decimal import Decimal
from .models import Habitacion, Reserva

class ReservaTest(TestCase):

    def setUp(self):
        self.habitacion = Habitacion.objects.create(
            numero=101,
            tipo="Doble",
            precio=85.00,
            disponible=True
        )

        self.reserva = Reserva.objects.create(
            habitacion=self.habitacion,
            cliente="Pedro Ruiz",
            fecha_entrada=date(2027, 7, 3),
            fecha_salida=date(2027, 7, 10)
        )

    def test_crear_habitacion(self):
        self.assertEqual(self.habitacion.numero, 101)

    def test_calcular_noches(self):
        self.assertEqual(self.reserva.noches, 7)

    def test_calcular_precio(self):
        self.assertEqual(
            self.reserva.precio_total,
            Decimal("595.00")
        )

    def test_fechas_incorrectas(self):
        reserva = Reserva(
            habitacion=self.habitacion,
            cliente="Juan Garcia",
            fecha_entrada=date(2027, 7, 15),
            fecha_salida=date(2027, 7, 12)
        )

        with self.assertRaises(ValidationError):
            reserva.full_clean()

    def test_reserva_solapada(self):
        reserva = Reserva(
            habitacion=self.habitacion,
            cliente="Maria Lopez",
            fecha_entrada=date(2027, 7, 5),
            fecha_salida=date(2027, 7, 8)
        )

        with self.assertRaises(ValidationError):
            reserva.full_clean()

class SeguridadTest(TestCase):

    def test_acceso_sin_login(self):
        respuesta = self.client.get("/reservas/")

        self.assertEqual(respuesta.status_code, 302)

    def test_acceso_administrador(self):
        from django.contrib.auth.models import User

        usuario = User.objects.create_user(
            username="admin_test",
            password="test12345",
            is_staff=True
        )

        self.client.force_login(usuario)

        respuesta = self.client.get("/reservas/")

        self.assertEqual(respuesta.status_code, 200)

    def test_acceso_cliente(self):
        from django.contrib.auth.models import User

        usuario = User.objects.create_user(
            username="cliente_test",
            password="test12345",
            is_staff=False
        )

        self.client.force_login(usuario)

        respuesta = self.client.get("/reservas/")

        self.assertEqual(respuesta.status_code, 302)        

    def test_cliente_no_puede_editar(self):
        from django.contrib.auth.models import User

        usuario = User.objects.create_user(
            username="cliente_editar",
            password="test12345",
            is_staff=False
        )

        self.client.force_login(usuario)

        respuesta = self.client.post("/reservas/editar/1/")

        self.assertEqual(respuesta.status_code, 302)

    def test_cliente_no_puede_eliminar(self):
        from django.contrib.auth.models import User

        usuario = User.objects.create_user(
            username="cliente_eliminar",
            password="test12345",
            is_staff=False
        )

        self.client.force_login(usuario)

        respuesta = self.client.post("/reservas/eliminar/1/")

        self.assertEqual(respuesta.status_code, 302)


class DisponibilidadTest(TestCase):

    def setUp(self):
        self.habitacion = Habitacion.objects.create(
            numero=101,
            tipo="Doble",
            precio=Decimal("85.00"),
            disponible=True
        )

        self.reserva = Reserva.objects.create(
            habitacion=self.habitacion,
            cliente="Cliente original",
            fecha_entrada=date(2027, 7, 3),
            fecha_salida=date(2027, 7, 10)
        )

    def test_reservas_consecutivas(self):
        reserva = Reserva(
            habitacion=self.habitacion,
            cliente="Cliente nuevo",
            fecha_entrada=date(2027, 7, 10),
            fecha_salida=date(2027, 7, 15)
        )

        reserva.full_clean()
        reserva.save()

        self.assertEqual(Reserva.objects.count(), 2)

    def test_reservas_distintas_habitaciones(self):
        otra_habitacion = Habitacion.objects.create(
            numero=102,
            tipo="Individual",
            precio=Decimal("55.00")
        )

        reserva = Reserva(
            habitacion=otra_habitacion,
            cliente="Otro cliente",
            fecha_entrada=date(2027, 7, 3),
            fecha_salida=date(2027, 7, 10)
        )

        reserva.full_clean()
        reserva.save()

        self.assertEqual(Reserva.objects.count(), 2)

    def test_editar_reserva_sin_conflicto(self):
        self.reserva.fecha_salida = date(2027, 7, 12)
        self.reserva.full_clean()
        self.reserva.save()

        self.assertEqual(self.reserva.noches, 9)

    def test_editar_reserva_con_conflicto(self):
        Reserva.objects.create(
            habitacion=self.habitacion,
            cliente="Segundo cliente",
            fecha_entrada=date(2027, 7, 12),
            fecha_salida=date(2027, 7, 15)
        )

        self.reserva.fecha_salida = date(2027, 7, 14)

        with self.assertRaises(ValidationError):
            self.reserva.full_clean()
            

class PostgreSQLTest(TestCase):

    @skipUnless(
        connection.vendor == "postgresql",
        "Prueba exclusiva de PostgreSQL"
    )
    def test_proteccion_reservas_solapadas(self):
        habitacion = Habitacion.objects.create(
            numero=201,
            tipo="Doble",
            precio=Decimal("85.00")
        )

        Reserva.objects.create(
            habitacion=habitacion,
            cliente="Cliente A",
            fecha_entrada=date(2027, 7, 1),
            fecha_salida=date(2027, 7, 10)
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reserva.objects.bulk_create([
                    Reserva(
                        habitacion=habitacion,
                        cliente="Cliente B",
                        fecha_entrada=date(2027, 7, 5),
                        fecha_salida=date(2027, 7, 8)
                    )
                ])