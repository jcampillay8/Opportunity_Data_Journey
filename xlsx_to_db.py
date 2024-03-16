import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.client_management.models import ClientData

def load_data():
    # Crea un DataFrame con los datos de tu tabla
    data = {
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Company Name': ['Tech Solutions Inc', 'Green Eco Group', 'Global Logistics', 'Food Master Ltd', 'Bright Ideas Inc', 'Servicios Informáticos Ltda', 'Construcciones y Asociados', 'Alimentos del Sur SA', 'Energía Solar Chilena', 'Distribuidora Nacional'],
        'Company ID Number': ['TS-123456', 'GEG-789012', 'GL-345678', 'FML-901234', 'BI-567890', 'SIL-123456', 'CA-789012', 'ADS-345678', 'ESC-901234', 'DN-567890'],
        'Company Type': ['Corporation', 'LLC', 'Partnership', 'Corporation', 'LLC', 'LLC', 'Corporation', 'Corporation', 'Partnership', 'LLC'],
        'Company Nationality': ['US', 'UK', 'China', 'France', 'Canada', 'Chile', 'Chile', 'Chile', 'Chile', 'Chile'],
        'Business Sector': ['Technology', 'Environmental', 'Transportation', 'Food Industry', 'Innovation', 'Technology', 'Construction', 'Food Industry', 'Renewable Energy', 'Distribution'],
        'Primary Contact': ['John Smith', 'Emily Johnson', 'Michael Brown', 'Sarah Lee', 'David Wilson', 'Pablo Martínez', 'María González', 'Juan Pérez', 'Carolina López', 'Pedro Rodríguez'],
        'Primary Email': ['john@example.com', 'emily@example.com', 'michael@example.com', 'sarah@example.com', 'david@example.com', 'pablo@example.com', 'maria@example.com', 'juan@example.com', 'carolina@example.com', 'pedro@example.com'],
        'Representatives': [10, 8, 12, 15, 7, 6, 10, 8, 5, 12],
        'Website': ['www.techsolutions.com', 'www.greenecogroup.com', 'www.globallogistics.com', 'www.foodmaster.com', 'www.brightideas.com', 'www.serviciosinformaticos.cl', 'www.construccionesyasociados.cl', 'www.alimentosdelsur.cl', 'www.energiasolarchilena.cl', 'www.distribuidoranacional.cl'],
        'Relationship Status': ['Active', 'Active', 'Active', 'Inactive', 'Active', 'Active', 'Active', 'Active', 'Inactive', 'Active'],
        'Notes': ['Leading provider of IT services', 'Specializes in sustainable energy solutions', 'International shipping and logistics', 'Gourmet food supplier', 'Cutting-edge technology development', 'Especializados en soluciones informáticas', 'Proyectos de construcción y remodelación', 'Productos alimenticios de alta calidad', 'Proyectos de energía solar', 'Distribución de productos diversos']
    }
    df = pd.DataFrame(data)

    # Itera sobre cada fila del DataFrame
    for index, row in df.iterrows():
        client = ClientData()
        client.company_name = row['Company Name']
        client.company_id_number = row['Company ID Number']
        client.company_type = row['Company Type']
        client.company_nationality = row['Company Nationality']
        client.business_sector = row['Business Sector']
        client.primary_contact = row['Primary Contact']
        client.primary_email = row['Primary Email']
        client.representatives = int(row['Representatives'])
        client.website = row['Website']
        client.relationship_status = row['Relationship Status']    
        client.notes = row['Notes']
        client.save()

load_data()
