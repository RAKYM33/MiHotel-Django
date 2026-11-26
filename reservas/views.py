from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Habitacion, Reserva
from datetime import date
from .forms import ReservaForm
from django.contrib.admin.views.decorators import staff_member_required
def inicio(request):
    habitaciones = Habitacion.objects.filter(disponible=True)

    entrada = request.GET.get("entrada", "")
    salida = request.GET.get("salida", "")
    error = None

    if request.method == "POST":
        entrada = request.POST.get("entrada", "")
        salida = request.POST.get("salida", "")
        cliente = request.POST.get("cliente", "").strip()
        habitacion_id = request.POST.get("habitacion")

        try:
            habitacion = Habitacion.objects.get(
                id=habitacion_id,
                disponible=True
            )

            reserva = Reserva(
                habitacion=habitacion,
                cliente=cliente,
                fecha_entrada=date.fromisoformat(entrada),
                fecha_salida=date.fromisoformat(salida)
            )

            reserva.full_clean()
            reserva.save()

            return redirect(request.path + "?exito=1")

        except ValidationError as e:
            error = " ".join(e.messages)

        except Habitacion.DoesNotExist:
            error = "La habitación no está disponible."

        except ValueError:
            error = "Los datos introducidos no son válidos."

    if (entrada or salida) and not error:
        try:
            fecha_entrada = date.fromisoformat(entrada)
            fecha_salida = date.fromisoformat(salida)

            if fecha_salida <= fecha_entrada:
                error = "La salida debe ser posterior a la entrada."
            else:
                reservas_ocupadas = Reserva.objects.filter(
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada
                )

                habitaciones = habitaciones.exclude(
                    id__in=reservas_ocupadas.values_list(
                        "habitacion_id", flat=True
                    )
                )

        except ValueError:
            error = "Introduce unas fechas válidas."

    if error:
        habitaciones = Habitacion.objects.none()

    return render(request, "reservas/inicio.html", {
        "habitaciones": habitaciones,
        "entrada": entrada,
        "salida": salida,
        "error": error,
        "exito": request.GET.get("exito")
    })

@staff_member_required
def listado_reservas(request):
    reservas = Reserva.objects.all().order_by("fecha_entrada")

    buscar = request.GET.get("buscar", "").strip()
    habitacion = request.GET.get("habitacion", "").strip()

    if buscar:
        reservas = reservas.filter(cliente__icontains=buscar)

    if habitacion:
        try:
            reservas = reservas.filter(habitacion__numero=int(habitacion))
        except ValueError:
            reservas = reservas.none()

    total_reservas = reservas.count()
    total_noches = sum(reserva.noches for reserva in reservas)
    total_ingresos = sum(reserva.precio_total for reserva in reservas)

    return render(request, "reservas/listado_reservas.html", {
        "reservas": reservas,
        "total_reservas": total_reservas,
        "total_noches": total_noches,
        "total_ingresos": total_ingresos,
        "buscar": buscar,
        "habitacion": habitacion
    })
@staff_member_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == "POST":
        reserva.delete()
        return redirect("/reservas/")

    return render(request, "reservas/eliminar_reserva.html", {
        "reserva": reserva
    })

@staff_member_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)

        if form.is_valid():
            form.save()
            return redirect("/reservas/")

    else:
        form = ReservaForm(instance=reserva)

    return render(request, "reservas/editar_reserva.html", {
        "form": form,
        "reserva": reserva
    })