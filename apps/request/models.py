from django.db import models
from django.contrib.auth.models import User

class CotizacionRealizada(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    formulario = models.CharField(max_length=200)
    nombre_proveedor = models.CharField(max_length=200)
    rut_proveedor = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    centro_costo = models.CharField(max_length=200)
    nombre_solicitante = models.CharField(max_length=200)
    nombre_autoriza = models.CharField(max_length=200)
    nombre_producto = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    descripcion_producto = models.TextField()
    hora_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_solicitud = models.DateField(auto_now_add=True)
