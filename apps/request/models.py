from django.db import models

class CotizacionRealizada(models.Model):
    User_Id = models.IntegerField()
    User_Name = models.CharField(max_length=200)
    Formulario = models.CharField(max_length=200)
    Nombre_Proveedor = models.CharField(max_length=200)
    Rut_Proveedor = models.CharField(max_length=200)
    Empresa = models.CharField(max_length=200)
    Area = models.CharField(max_length=200)
    Centro_Costo = models.CharField(max_length=200)
    Nombre_Solicitante = models.CharField(max_length=200)
    Nombre_Autoriza = models.CharField(max_length=200)
    hora_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

class CotizacionRealizada_Productos(models.Model):
    ID_OC = models.ForeignKey(CotizacionRealizada, on_delete=models.CASCADE)
    Nombre_Producto = models.CharField(max_length=200)
    Cantidad = models.IntegerField()
    Descripcion_Producto = models.CharField(max_length=200)

class CotizacionRealizada_Archivos(models.Model):
    ID_OC = models.ForeignKey(CotizacionRealizada, on_delete=models.CASCADE)
    File_Number = models.IntegerField()
    File_Name = models.CharField(max_length=200)
    File_Type = models.CharField(max_length=200)

class Estado_Solicitudes(models.Model):
    ID_OC = models.ForeignKey(CotizacionRealizada, on_delete=models.CASCADE)
    Request_Status = models.CharField(max_length=200, default='Solicitud Creada')
    Solicitud_Creada = models.BooleanField(default=True)
    Solicitud_Revision = models.BooleanField(default=False)
    Solicitud_Aprobada = models.BooleanField(default=False)
    Solicitud_Finalizada = models.BooleanField(default=False)
    Hora_Inicio_Solicitud_Creada = models.DateTimeField(auto_now_add=True)
    Hora_Inicio_Solicitud_Revision = models.DateTimeField(null=True, blank=True)
    Hora_Inicio_Solicitud_Aprobada = models.DateTimeField(null=True, blank=True)
    Hora_Inicio_Solicitud_Finalizada = models.DateTimeField(null=True, blank=True)

