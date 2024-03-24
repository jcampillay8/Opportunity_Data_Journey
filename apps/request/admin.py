from django.contrib import admin
from .models import CotizacionRealizada, CotizacionRealizada_Productos, CotizacionRealizada_Archivos, Estado_Solicitudes

admin.site.register(CotizacionRealizada)
admin.site.register(CotizacionRealizada_Productos)
admin.site.register(CotizacionRealizada_Archivos)
admin.site.register(Estado_Solicitudes)
