import pandas as pd
import os
import django
import random

# Configurar la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.request.models import CotizacionRealizada

# Lista de nombres y proveedores
nombres_proveedores = {
    "Juan": "Alimentos del Sur SA",
    "Pedro": "Alimentos del Sur SA",
    "Elena": "Alimentos del Sur SA",
    "María": "Construcciones y Asociados",
    "Teresa": "Construcciones y Asociados",
    "Ana": "Servicios Informáticos Ltda",
    "Luis": "Servicios Informáticos Ltda",
    "José": "Servicios Informáticos Ltda",
    "Sofía": "Bright Ideas Inc",
    "Laura": "Bright Ideas Inc",
    "Diego": "Bright Ideas Inc",
    "Carmen": "Bright Ideas Inc",
    "Carlos": "Food Master Ltd",
    "Pablo": "Food Master Ltd",
    "Manuel": "Food Master Ltd",
    "Marta": "Global Logistics",
    "Javier": "Global Logistics",
    "Antonio": "Green Eco Group",
    "Ana María": "Green Eco Group",
    "Isabel": "Energía Solar Chilena"
}

# Generar un conjunto único de nombres de usuario
nombres_usuario = list(nombres_proveedores.keys())

# Asignar un ID único a cada nombre de usuario
id_usuario = list(range(1, len(nombres_usuario) + 1))

# Mapear nombres de usuario a IDs
nombre_usuario_a_id = dict(zip(nombres_usuario, id_usuario))

# Generar nombres aleatorios
nombres = random.choices(nombres_usuario, k=70)

# Mapear nombres a IDs para User_Id
user_ids = [nombre_usuario_a_id[nombre] for nombre in nombres]

# Generar tipo de cotización aleatorio
tipo_cotizacion = random.choices(["Cotización Realizada", "Solicitud de Cotización"], k=70)

# Asignar proveedores según los nombres
proveedores = [nombres_proveedores[nombre] for nombre in nombres]

# Obtener datos adicionales para cada proveedor
datos_proveedores = {
    "Alimentos del Sur SA": {"Rut_Proveedor": "123456789-0", "Centro_Costo": "AC001", "Nombre_Solicitante": "Juan", "Nombre_Autoriza": "Pedro"},
    "Construcciones y Asociados": {"Rut_Proveedor": "987654321-0", "Centro_Costo": "CC002", "Nombre_Solicitante": "María", "Nombre_Autoriza": "Teresa"},
    "Servicios Informáticos Ltda": {"Rut_Proveedor": "567890123-0", "Centro_Costo": "CI003", "Nombre_Solicitante": "Ana", "Nombre_Autoriza": "Luis"},
    "Bright Ideas Inc": {"Rut_Proveedor": "456789012-0", "Centro_Costo": "BI004", "Nombre_Solicitante": "Sofía", "Nombre_Autoriza": "Laura"},
    "Food Master Ltd": {"Rut_Proveedor": "234567890-0", "Centro_Costo": "FM005", "Nombre_Solicitante": "Carlos", "Nombre_Autoriza": "Pablo"},
    "Global Logistics": {"Rut_Proveedor": "345678901-0", "Centro_Costo": "GL006", "Nombre_Solicitante": "Marta", "Nombre_Autoriza": "Javier"},
    "Green Eco Group": {"Rut_Proveedor": "678901234-0", "Centro_Costo": "GE007", "Nombre_Solicitante": "Antonio", "Nombre_Autoriza": "Ana María"},
    "Energía Solar Chilena": {"Rut_Proveedor": "890123456-0", "Centro_Costo": "ES008", "Nombre_Solicitante": "Isabel", "Nombre_Autoriza": "Elena"}
}

rut_proveedor = [datos_proveedores[prov]["Rut_Proveedor"] for prov in proveedores]
centro_costo = [datos_proveedores[prov]["Centro_Costo"] for prov in proveedores]
nombre_solicitante = [datos_proveedores[prov]["Nombre_Solicitante"] for prov in proveedores]
nombre_autoriza = [datos_proveedores[prov]["Nombre_Autoriza"] for prov in proveedores]

# Generar valores aleatorios para la columna "Empresa"
empresa = random.choices(["DTS", "ETICSA"], k=70)

# Generar valores aleatorios para la columna "Area" basados en la empresa
departamento = []
for emp in empresa:
    if emp == "DTS":
        departamento.append(random.choice(["SERVICIOS", "PROYECTOS"]))
    elif emp == "ETICSA":
        departamento.append(random.choice(["SERVICIOS", "INTEGRACIÓN"]))

# Crear DataFrame
df = pd.DataFrame({
    "User_Id": user_ids,  # Usamos los IDs de usuario en lugar de los nombres
    "User_Name": nombres,
    "Formulario": tipo_cotizacion,
    "Nombre_Proveedor": proveedores,
    "Rut_Proveedor": rut_proveedor,
    "Empresa": empresa,
    "Area": departamento,
    "Centro_Costo": centro_costo,
    "Nombre_Solicitante": nombre_solicitante,
    "Nombre_Autoriza": nombre_autoriza
})


# Cambiar el nombre de la columna 'Departamento' a 'Area'
df.rename(columns={'Departamento': 'Area'}, inplace=True)

# Cambiar el orden de las columnas para que coincida con el orden en 'data'
column_order = ['User_Id', 'User_Name', 'Formulario', 'Nombre_Proveedor', 'Rut_Proveedor', 'Empresa', 'Area', 'Centro_Costo', 'Nombre_Solicitante', 'Nombre_Autoriza']
df = df[column_order]

# Iterar sobre cada fila del DataFrame y crear los objetos CotizacionRealizada
for index, row in df.iterrows():
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
    cotizacion.save()


# import pandas as pd
# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# django.setup()

# from apps.request.models import CotizacionRealizada

# def load_data():
#     # Crea un DataFrame con los datos de tu tabla
#     data = {
#         'User_Id': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
#         'User_Name': ['Juan', 'Pedro', 'Elena', 'María', 'Teresa', 'Ana', 'Luis', 'José', 'Sofía', 'Laura', 'Diego', 'Carmen', 'Carlos', 'Pablo', 'Manuel', 'Marta', 'Javier', 'Antonio', 'Ana María', 'Isabel'],
#         'Formulario': ['Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada', 'Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada', 'Cotización Realizada', 'Solicitud de Cotización', 'Solicitud de Cotización', 'Cotización Realizada', 'Cotización Realizada'],
#         'Nombre_Proveedor': ['Alimentos del Sur SA', 'Alimentos del Sur SA', 'Alimentos del Sur SA', 'Construcciones y Asociados', 'Construcciones y Asociados', 'Servicios Informáticos Ltda', 'Servicios Informáticos Ltda', 'Servicios Informáticos Ltda', 'Bright Ideas Inc', 'Bright Ideas Inc', 'Bright Ideas Inc', 'Bright Ideas Inc', 'Food Master Ltd', 'Food Master Ltd', 'Food Master Ltd', 'Global Logistics', 'Global Logistics', 'Green Eco Group', 'Green Eco Group', 'Energía Solar Chilena'],
#         'Rut_Proveedor': ['76.101.202-9', '76.101.202-9', '76.101.202-9', '76.202.303-8', '76.202.303-8', '76.303.404-8', '76.303.404-8', '76.303.404-8', '76.404.505-6', '76.404.505-6', '76.404.505-6', '76.404.505-6', '76.606.707-4', '76.606.707-4', '76.606.707-4', '76.707.808-3', '76.707.808-3', '76.707.808-5', '76.707.808-5', '76.808.909-2'],
#         'Empresa': ['DTS', 'DTS', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'DTS', 'ETICSA', 'ETICSA', 'DTS', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'ETICSA', 'DTS', 'ETICSA', 'ETICSA'],
#         'Area': ['PROYECTOS', 'SERVICIOS', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'SERVICIOS', 'PROYECTOS', 'SERVICIOS', 'SERVICIOS', 'SERVICIOS', 'INTEGRACIÓN', 'SERVICIOS', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'INTEGRACIÓN', 'PROYECTOS', 'INTEGRACIÓN', 'SERVICIOS'],
#         'Centro_Costo': ['ADS-345678', 'ADS-345678', 'ADS-345678', 'CA-789012', 'CA-789012', 'SIL-123456', 'SIL-123456', 'SIL-123456', 'BI-567890', 'BI-567890', 'BI-567890', 'BI-567890', 'FML-901234', 'FML-901234', 'FML-901234', 'GL-345678', 'GL-345678', 'GEG-789012', 'GEG-789012', 'ESC-901234'],
#         'Nombre_Solicitante': ['John', 'James', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen', 'Nancy', 'Lisa'],
#         'Nombre_Autoriza': ['Paul', 'Mark', 'George', 'Steven', 'Kenneth', 'Andrew', 'Edward', 'Joshua', 'Brian', 'Kevin', 'Mary', 'Donna', 'Michelle', 'Laura', 'Emily', 'Deborah', 'Amy', 'Rebecca', 'Kimberly', 'Melissa']
#     }
#     df = pd.DataFrame(data)

#     # Itera sobre cada fila del DataFrame
#     for index, row in df.iterrows():
#         # Crea un nuevo objeto CotizacionRealizada con los datos de la fila
#         cotizacion = CotizacionRealizada(
#             User_Id=row['User_Id'],
#             User_Name=row['User_Name'],
#             Formulario=row['Formulario'],
#             Nombre_Proveedor=row['Nombre_Proveedor'],
#             Rut_Proveedor=row['Rut_Proveedor'],
#             Empresa=row['Empresa'],
#             Area=row['Area'],
#             Centro_Costo=row['Centro_Costo'],
#             Nombre_Solicitante=row['Nombre_Solicitante'],
#             Nombre_Autoriza=row['Nombre_Autoriza']
#         )
#         # Guarda el objeto en la base de datos
#         cotizacion.save()

# load_data()
