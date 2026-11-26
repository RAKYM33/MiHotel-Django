from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva

        fields = [
            "cliente",
            "habitacion",
            "fecha_entrada",
            "fecha_salida"
        ]

        widgets = {
            "fecha_entrada": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"}
            ),
            "fecha_salida": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"}
            ),
        }