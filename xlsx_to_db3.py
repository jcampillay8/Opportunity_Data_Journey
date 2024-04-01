import pandas as pd
import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.request.models import CotizacionRealizada, CotizacionRealizada_Productos

def load_data():
    productos_energia_solar_chilena = {
        "Paneles solares fotovoltaicos": "Paneles solares para la captación de energía solar y su conversión en energía eléctrica.",
        "Inversores solares": "Inversores fotovoltaicos para convertir la corriente continua generada por los paneles solares en corriente alterna.",
        "Estructuras de montaje": "Soportes y estructuras para la instalación y fijación de paneles solares en techos o terrenos.",
        "Sistemas de monitoreo solar": "Sistemas de supervisión y monitoreo del rendimiento de instalaciones solares fotovoltaicas.",
        "Baterías de almacenamiento solar": "Baterías recargables para almacenar la energía generada por paneles solares y utilizarla en momentos de baja radiación solar.",
        "Cableado y conectores solares": "Cables, conectores y accesorios especializados para sistemas de energía solar.",
        "Reguladores de carga": "Dispositivos para controlar la carga de las baterías solares y proteger los equipos de sobrecargas.",
        "Luminarias solares": "Lámparas y sistemas de iluminación autónomos alimentados por energía solar para exteriores.",
        "Calefacción solar de agua": "Sistemas de calentamiento de agua mediante paneles solares térmicos.",
        "Bombas solares": "Bombas de agua alimentadas por energía solar para riego agrícola, suministro de agua potable y sistemas de fontanería.",
        "Sistemas de bombeo solar": "Sistemas completos de bombeo de agua accionados por energía solar.",
        "Calentadores de piscinas solares": "Calentadores de agua para piscinas que utilizan energía solar térmica para elevar la temperatura del agua.",
        "Iluminación solar urbana": "Sistemas de alumbrado público alimentados por energía solar para espacios urbanos y rurales.",
        "Sistemas de energía solar off-grid": "Sistemas autónomos de generación de energía solar para instalaciones aisladas de la red eléctrica.",
        "Sistemas de energía solar on-grid": "Sistemas conectados a la red eléctrica para la venta de excedentes de energía generada por paneles solares.",
        "Sistemas de energía solar híbrida": "Sistemas que combinan energía solar con otras fuentes de energía, como eólica o diesel, para garantizar un suministro estable.",
        "Seguidores solares": "Dispositivos mecánicos que siguen la trayectoria del sol para maximizar la captación de energía solar.",
        "Sistemas solares portátiles": "Kits y dispositivos solares compactos y portátiles para carga de dispositivos electrónicos en actividades al aire libre.",
        "Sistemas de energía solar para telecomunicaciones": "Soluciones energéticas renovables para torres de telecomunicaciones y estaciones base.",
        "Sistemas de refrigeración solar": "Sistemas de refrigeración alimentados por energía solar para conservar alimentos y medicamentos en zonas sin acceso a la red eléctrica.",
    }

    # Generar listas de productos, cantidad y descripción para Energía Solar Chilena
    productos_energia_solar_chilena_seleccionados = random.choices(list(productos_energia_solar_chilena.keys()), k=35)
    cantidades_energia_solar_chilena = [random.randint(1, 100) for _ in range(35)]
    descripciones_energia_solar_chilena = [productos_energia_solar_chilena[nombre] for nombre in productos_energia_solar_chilena_seleccionados]

    # Crear DataFrame df_productos para Energía Solar Chilena
    df_productos_energia_solar_chilena = pd.DataFrame({
        "Nombre_Producto": productos_energia_solar_chilena_seleccionados,
        "Cantidad": cantidades_energia_solar_chilena,
        "Descripcion_Producto": descripciones_energia_solar_chilena
    })

    valores_id_oc = [49,85,96,107]
    id_oc_id = random.choices(valores_id_oc, k=len(df_productos_energia_solar_chilena))
    df_productos_energia_solar_chilena["ID_OC_id"] = id_oc_id

    df = df_productos_energia_solar_chilena
    # Itera sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Crea un nuevo objeto CotizacionRealizada_Productos con los datos de la fila
        cotizacion_producto = CotizacionRealizada_Productos(
            #ID_OC_id=CotizacionRealizada.objects.get(id=row['ID_OC_id']),
            Nombre_Producto=row['Nombre_Producto'],
            Cantidad=row['Cantidad'],
            Descripcion_Producto=row['Descripcion_Producto'],
            ID_OC_id=row['ID_OC_id'],
        )
        # Guarda el objeto en la base de datos
        cotizacion_producto.save()

load_data()
