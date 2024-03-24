import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.request.models import CotizacionRealizada, CotizacionRealizada_Productos

def load_data():
    # Carga el archivo csv en un DataFrame
    df = pd.read_csv('fake_data_sp_global.csv')

    # Itera sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Crea un nuevo objeto CotizacionRealizada_Productos con los datos de la fila
        cotizacion_producto = CotizacionRealizada_Productos(
            ID_OC=CotizacionRealizada.objects.get(id=row['ID_OC']),
            Nombre_Producto=row['Nombre_Producto'],
            Cantidad=row['Cantidad'],
            Descripcion_Producto=row['Descripcion_Producto']
        )
        # Guarda el objeto en la base de datos
        cotizacion_producto.save()

load_data()
