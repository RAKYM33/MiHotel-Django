from django.db import models
from django.core.exceptions import ValidationError


class Habitacion(models.Model):
    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"


class Reserva(models.Model):
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT
    )
    cliente = models.CharField(max_length=100)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()

    def clean(self):
        if not self.fecha_entrada or not self.fecha_salida:
            return

        if self.fecha_salida <= self.fecha_entrada:
            raise ValidationError(
                "La fecha de salida debe ser posterior a la entrada."
            )

        conflictos = Reserva.objects.filter(
            habitacion_id=self.habitacion_id,
            fecha_entrada__lt=self.fecha_salida,
            fecha_salida__gt=self.fecha_entrada
        ).exclude(pk=self.pk)

        if conflictos.exists():
            raise ValidationError(
                "Esta habitación ya está reservada para esas fechas."
            )
    @property
    def noches(self):
        return (self.fecha_salida - self.fecha_entrada).days

    @property
    def precio_total(self):
        return self.noches * self.habitacion.precio
    def __str__(self):
        return f"{self.cliente} - {self.habitacion}"