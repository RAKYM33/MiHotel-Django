from django.contrib import admin
from django.urls import path
from reservas.views import inicio, listado_reservas, eliminar_reserva, editar_reserva

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio),
    path("reservas/", listado_reservas),
    path("reservas/eliminar/<int:reserva_id>/", eliminar_reserva),
    path("reservas/editar/<int:reserva_id>/", editar_reserva),
]