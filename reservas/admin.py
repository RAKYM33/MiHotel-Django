from django.contrib import admin
from .models import Habitacion, Reserva


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ("numero", "tipo", "precio", "disponible")
    list_filter = ("tipo", "disponible")
    search_fields = ("numero", "tipo")
    ordering = ("numero",)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "habitacion",
        "fecha_entrada",
        "fecha_salida",
        "noches",
        "precio_total"
    )
    list_filter = ("fecha_entrada", "fecha_salida")
    search_fields = ("cliente", "habitacion__numero")
    ordering = ("fecha_entrada",)