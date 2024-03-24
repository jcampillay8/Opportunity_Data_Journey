import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.request.models import CotizacionRealizada, CotizacionRealizada_Archivos

def load_data():
    # Carga el archivo csv en un DataFrame
    df = pd.read_csv('result.csv')

    # Itera sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Crea un nuevo objeto CotizacionRealizada_Archivos con los datos de la fila
        cotizacion_archivo = CotizacionRealizada_Archivos(
            ID_OC=CotizacionRealizada.objects.get(id=row['ID_OC_id']),
            File_Number=row['File_Number'],
            File_Name=row['File_Name'],
            File_Type=row['File_type']
        )
        # Guarda el objeto en la base de datos
        cotizacion_archivo.save()

load_data()
