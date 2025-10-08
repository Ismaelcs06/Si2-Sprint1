from django.db import models

class Caso(models.Model):
     
     ESTADO_CHOICES = [
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
     ]
     PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),       
        ('Media', 'Media'),
        ('Alta', 'Alta'),
     ]
     nro_caso = models.CharField(max_length=20)
     fecha_inicio = models.DateField()
     fecha_finalizacion = models.DateField(null=True, blank=True)
     estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Abierto')
     descripcion = models.TextField()
     apelaciones = models.TextField()
     tipo_de_caso = models.CharField(max_length=100)
     prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='Baja')
     creado_en = models.DateTimeField(auto_now_add=True)
     actualizado_en = models.DateTimeField(auto_now=True)

     def __str__(self):
        return self.nro_caso


class Expediente(models.Model):
    EXPEDIENTE_CHOICES = [
        ('Proceso', 'Proceso'),
        ('Cerrado', 'Cerrado'),
    ]
    nro_expediente = models.CharField(max_length=20)
    fecha_de_creacion = models.DateField()
    Fecha_de_cierre = models.DateField(null=True, blank=True)
    autoridad = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=EXPEDIENTE_CHOICES, default='Proceso')
    observaciones = models.TextField()
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='expedientes')

    class Meta:
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        unique_together = ("caso", "nro_expediente")
        ordering = ["caso", "nro_expediente"]

    def __str__(self):
        return f"{self.caso.nro_caso} / {self.nro_expediente}"

