import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.request.models import CotizacionRealizada

def load_data():
    # Crea un DataFrame con los datos de tu tabla
    data = {
        'User_Id': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
        'User_Name': ['Juan', 'Pedro', 'Elena', 'María', 'Teresa', 'Ana', 'Luis', 'José', 'Sofía', 'Laura', 'Diego', 'Carmen', 'Carlos', 'Pablo', 'Manuel', 'Marta', 'Javier', 'Antonio', 'Ana María', 'Isabel'],
        'Formulario': ['Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada', 'Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada', 'Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada'],
        'Nombre_Proveedor': ['Alimentos del Sur SA', 'Alimentos del Sur SA', 'Alimentos del Sur SA', 'Construcciones y Asociados', 'Construcciones y Asociados', 'Servicios Informáticos Ltda', 'Servicios Informáticos Ltda', 'Servicios Informáticos Ltda', 'Bright Ideas Inc', 'Bright Ideas Inc', 'Bright Ideas Inc', 'Bright Ideas Inc', 'Food Master Ltd', 'Food Master Ltd', 'Food Master Ltd', 'Global Logistics', 'Global Logistics', 'Green Eco Group', 'Green Eco Group', 'Energía Solar Chilena'],
        'Rut_Proveedor': ['76.101.202-9', '76.101.202-9', '76.101.202-9', '76.202.303-8', '76.202.303-8', '76.303.404-8', '76.303.404-8', '76.303.404-8', '76.404.505-6', '76.404.505-6', '76.404.505-6', '76.404.505-6', '76.606.707-4', '76.606.707-4', '76.606.707-4', '76.707.808-3', '76.707.808-3', '76.707.808-5', '76.707.808-5', '76.808.909-2'],
        'Empresa': ['DTS', 'DTS', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'DTS', 'ETICSA', 'ETICSA', 'DTS', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'DTS', 'ETICSA', 'ETICSA'],
        'Area': ['PROYECTOS', 'SERVICIOS', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'SERVICIOS', 'PROYECTOS', 'SERVICIOS', 'SERVICIOS', 'SERVICIOS', 'INTEGRACIÓN', 'SERVICIOS', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'PROYECTOS', 'INTEGRACIÓN', 'SERVICIOS'],
        'Centro_Costo': ['ADS-345678', 'ADS-345678', 'ADS-345678', 'CA-789012', 'CA-789012', 'SIL-123456', 'SIL-123456', 'SIL-123456', 'BI-567890', 'BI-567890', 'BI-567890', 'BI-567890', 'FML-901234', 'FML-901234', 'FML-901234', 'GL-345678', 'GL-345678', 'GEG-789012', 'GEG-789012', 'ESC-901234'],
        'Nombre_Solicitante': ['John', 'James', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen', 'Nancy', 'Lisa'],
        'Nombre_Autoriza': ['Paul', 'Mark', 'George', 'Steven', 'Kenneth', 'Andrew', 'Edward', 'Joshua', 'Brian', 'Kevin', 'Mary', 'Donna', 'Michelle', 'Laura', 'Emily', 'Deborah', 'Amy', 'Rebecca', 'Kimberly', 'Melissa']
    }
    df = pd.DataFrame(data)

    # Itera sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Crea un nuevo objeto CotizacionRealizada con los datos de la fila
        cotizacion = CotizacionRealizada(
            User_Id=row['User_Id'],
            User_Name=row['User_Name'],
            Formulario=row['Formulario'],
            Nombre_Proveedor=row['Nombre_Proveedor'],
            Rut_Proveedor=row['Rut_Proveedor'],
            Empresa=row['Empresa'],
            Area=row['Area'],
            Centro_Costo=row['Centro_Costo'],
            Nombre_Solicitante=row['Nombre_Solicitante'],
            Nombre_Autoriza=row['Nombre_Autoriza']
        )
        # Guarda el objeto en la base de datos
        cotizacion.save()

load_data()
