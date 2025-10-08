from django import forms
from .models import Caso, Expediente
from datetime import date

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = [
            'nro_caso',
            'fecha_inicio',
            'fecha_finalizacion',
            'estado',
            'descripcion',
            'apelaciones',
            'tipo_de_caso',
            'prioridad',
        ]
        widgets = {
            'fecha_inicio': forms.SelectDateWidget(years=range(1900, date.today().year + 10)),
            'fecha_finalizacion': forms.SelectDateWidget(years=range(1900, date.today().year + 10)),
            'descripcion': forms.Textarea(),
            'apelaciones': forms.Textarea(),
          

        }

class ExpedienteForm(forms.ModelForm):
    class Meta:
        model = Expediente
        fields = [
            'nro_expediente',
            'fecha_de_creacion',
            'Fecha_de_cierre',
            'autoridad',
            'estado',
            'observaciones',
            'caso',
        ]
        widgets = {
            'fecha_de_creacion': forms.SelectDateWidget(years=range(1900, date.today().year + 10)),
            'Fecha_de_cierre': forms.SelectDateWidget(years=range(1900, date.today().year + 10)),
            'observaciones': forms.Textarea(),
        }        