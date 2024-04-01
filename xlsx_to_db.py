# Importando las bibliotecas necesarias
import os
import django
import pandas as pd
from django.conf import settings

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

# Importar el modelo CotizacionRealizada
from apps.request.models import CotizacionRealizada

# Leer el archivo CSV
df_data_solicitudes = pd.read_csv('data_solicitudes_date.csv')

# Convertir 'fecha_solicitud' y 'hora_solicitud' a datetime
df_data_solicitudes['fecha_solicitud'] = pd.to_datetime(df_data_solicitudes['fecha_solicitud'])
df_data_solicitudes['hora_solicitud'] = pd.to_datetime(df_data_solicitudes['hora_solicitud'])

# Iterar sobre las filas del DataFrame
for index, row in df_data_solicitudes.iterrows():
    # Obtener el objeto CotizacionRealizada con el id correspondiente
    cotizacion = CotizacionRealizada.objects.get(id=row['id'])
    
    # Actualizar los campos 'fecha_solicitud' y 'hora_solicitud'
    cotizacion.fecha_solicitud = row['fecha_solicitud']
    cotizacion.hora_solicitud = row['hora_solicitud']
    
    # Guardar los cambios
    cotizacion.save()

print("Los campos 'fecha_solicitud' y 'hora_solicitud' se actualizaron correctamente.")
