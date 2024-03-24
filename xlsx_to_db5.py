import os
import django
import pandas as pd
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.request.models import CotizacionRealizada, Estado_Solicitudes

def load_data():
    # Crea un DataFrame con los datos de tu tabla
    data = {
        'ID_OC_id': list(range(13, 33)),
        'Request_Status': ['Solicitud Creada'] * 20,
        'Solicitud_Creada': [True] * 20,
        'Solicitud_Revision': [False] * 20,
        'Solicitud_Aprobada': [False] * 20,
        'Solicitud_Finalizada': [False] * 20,
        'Hora_Inicio_Solicitud_Creada': [datetime.now()] * 20,
        'Hora_Inicio_Solicitud_Revision': [None] * 20,
        'Hora_Inicio_Solicitud_Aprobada': [None] * 20,
        'Hora_Inicio_Solicitud_Finalizada': [None] * 20
    }
    df = pd.DataFrame(data)

    # Itera sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Crea un nuevo objeto Estado_Solicitudes con los datos de la fila
        estado_solicitud = Estado_Solicitudes(
            ID_OC=CotizacionRealizada.objects.get(id=row['ID_OC_id']),
            Request_Status=row['Request_Status'],
            Solicitud_Creada=row['Solicitud_Creada'],
            Solicitud_Revision=row['Solicitud_Revision'],
            Solicitud_Aprobada=row['Solicitud_Aprobada'],
            Solicitud_Finalizada=row['Solicitud_Finalizada'],
            Hora_Inicio_Solicitud_Creada=row['Hora_Inicio_Solicitud_Creada'],
            Hora_Inicio_Solicitud_Revision=row['Hora_Inicio_Solicitud_Revision'],
            Hora_Inicio_Solicitud_Aprobada=row['Hora_Inicio_Solicitud_Aprobada'],
            Hora_Inicio_Solicitud_Finalizada=row['Hora_Inicio_Solicitud_Finalizada']
        )
        # Guarda el objeto en la base de datos
        estado_solicitud.save()

load_data()
