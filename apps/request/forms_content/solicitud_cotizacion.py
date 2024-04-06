import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback, dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
import traceback
import dash_daq as daq
from datetime import date
from dash.dash_table.Format import Group
import pandas as pd
import os
import boto3
from django.conf import settings

df_solicitud_cotizacion = pd.DataFrame(columns=['User_Id', 'User_Name','Formulario', 'Nombre Proveedor', 'Rut_Proveedor', 'Empresa', 'Area', 'Centro Costo', 'Nombre Solicitante', 'Nombre de Quién Autoriza'])
df_solicitud_cotizacion_productos = pd.DataFrame(columns=['Nombre Producto', 'Cantidad', 'Descripción Producto'])


def form_solicitud_cotizacion(selected_company):
    return[
    html.Br(),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((
            dcc.Markdown(f''' ## COTIZACIÓN REALIZADA ''', className="text-center"),
        ),width=10),
        dbc.Col((),width=1),
    ]),
    
    dbc.Row([
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
            dbc.Row([
            dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### NOMBRE PROVEEDOR: '''),
            ]), md=12, lg=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_proveedor',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), md=12, lg=9),

                ])
            ),width=10),
            dbc.Col(width=1),
        ]),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                                dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### RUT PROVEEDOR: '''),
            ]), md=12, lg=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_rut_proveedor',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), md=12, lg=9),
                ])
            ),width=10),
            dbc.Col(width=1),

        ]),
    
        dbc.Row([    
        dbc.Col(width=1),
        dbc.Col((html.Div([
            html.Div(style={'height': '20px'}),  # Add a space
    
            # dbc.Row([
            #     dbc.Col(dcc.Markdown(''' ### EMPRESA: '''), md=12, lg=3),
            #     dbc.Col(dcc.Dropdown(id='empresa-dropdown', options=[{'label': i, 'value': i} for i in ['ETICSA', 'DTS']]), md=12, lg=9),
            # ]),
            html.Div(style={'height': '20px'}),  # Add a space between the dropdowns
            dbc.Row([
                dbc.Col(dcc.Markdown(''' ### ÁREA: '''), md=12, lg=3),
                #dbc.Col(dcc.Dropdown(id='area-dropdown'), md=12, lg=9),
                dbc.Col(dcc.Dropdown(selected_company, id='area-dropdown'), md=12, lg=9),
            ]),
            ])),width=10),
        dbc.Col(width=1)
    ]),
            dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                                dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### CENTRO COSTO: '''),
            ]), md=12, lg=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_centro_costo',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), md=12, lg=9),
                ])
            ),width=10),
            dbc.Col(width=1),

        ]),
                dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                                dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### NOMBRE SOLICITANTE: '''),
            ]), md=12, lg=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_solicitante',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), md=12, lg=9),
                ])
            ),width=10),
            dbc.Col(width=1),

        ]),
         dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                                dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### NOMBRE DE QUIÉN AUTORIZA: '''),
            ]), md=12, lg=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_autoriza',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), md=12, width=9, lg=9),
                ])
            ),width=10),
            dbc.Col(width=1),

        ]),

        html.Div(style={'height': '40px'}),  # Add a space
                    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((
            dcc.Markdown(f''' ## DESGLOSE COMPRA (OPCIONAL) ''', className="text-center"),
        ),width=10),
        dbc.Col((),width=1),
    ]),
                   dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
            dbc.Row([
            dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### NOMBRE PRODUCTO: '''),
            ]), md=12, lg=2),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_producto',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), md=12, lg=6),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### CANTIDAD: '''),
            ]), md=12, lg=2),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_cantidad',
                    placeholder='Enter a value...',
                    type='number',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), md=12, lg=2),
            
                ])
            ),width=10),
            dbc.Col(width=1),
        ]),
        html.Div(style={'height': '40px'}),  # Add a space
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
            dcc.Markdown(''' ### DESCRIPCIÓN PRODUCTO: '''),

            ),width=10),
            dbc.Col(width=1),

        ]),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dcc.Textarea(
                id = 'input_descripcion_producto',
                placeholder='Describa el ítem...',
                style={'width': '100%'}
            )
            ),width=10),
            dbc.Col(width=1),

        ]),
            dbc.Row([
        dbc.Col(width=1),
        dbc.Col((
            dash_table.DataTable(
                id='table_producto',
                columns=[{"name": i, "id": i} for i in df_solicitud_cotizacion_productos.columns],
                data=df_solicitud_cotizacion_productos.to_dict('records'),
                editable=True,
                row_deletable=True,
                style_data={
                    'if': {'column_id': 'Descripción Producto'},
                    'whiteSpace': 'normal',
                     'height': 'auto',
                },
                style_cell_conditional=[
        {
            'if': {'column_id': 'Descripción Producto'},
            'textAlign': 'left',
        },
        {
            'if': {'column_id': 'Nombre Producto'},
            'textAlign': 'center',
        },
        {
            'if': {'column_id': 'Cantidad'},
            'textAlign': 'center',
        }
    ],
                
            ),
        ), width=10),
        dbc.Col(width=1),
    ]),
    html.Div(style={'height': '20px'}),  # Add a space
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col((
            dbc.Button('Agregar Producto', id='editing-rows-button', n_clicks=0),
        ), width=10),
        dbc.Col(width=1),
    ]),
        html.Div(style={'height': '40px'}),  # Add a space
        dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((
            dcc.Markdown(f''' ## ADJUNTAR DOCUMENTOS  ''', className="text-center"),
        ),width=10),
        dbc.Col((),width=1),
    ]),
    dbc.Row([    
        dbc.Col(width=1),
        dbc.Col((html.Div([
            html.Div(style={'height': '40px'}),  
            dbc.Row([
                dbc.Col(html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },

        multiple=True
    ),
    dcc.Store(id='store-data-upload'),
    html.Div(id='output-data-upload', children=dash_table.DataTable(id='data-table', row_deletable=True)),
    # html.Button('Save', id='save-button'),
    html.Div()
    ]), width=12),
                
            ]),
            ])),width=10),
        dbc.Col(width=1)
    ]),




        html.Div(style={'height': '40px'}),  # Add a space
        dbc.Row([
        dbc.Col(width=4),
        dbc.Col(dbc.Button('SAVE DATA', id='save-button', n_clicks=0), width=4),
        dbc.Col(width=4),


    ]),
        
            dbc.Col(width=1),
    ]),
        
    

    ]


def send_email(user_email):
    subject = "Solicitud 'Cotización Realizada' ha sido correctamente generada y enviada"
    message = """
    Estimado cliente,

    Nos complace informarle que su solicitud de cotización ha sido generada y enviada con éxito. Agradecemos su confianza en nuestros servicios y nos esforzamos por cumplir con sus expectativas.

    Si tiene alguna pregunta o necesita más información, no dude en ponerse en contacto con nosotros. Estamos a su disposición para ayudarle.

    Saludos cordiales,

    SP Global
    """
    email = EmailMessage(
        subject,
        message,
        "no-contestar@inbox.mailtrap.io",
        [user_email],
        reply_to=[user_email]
    )
    try:
        email.send()
    except Exception as e:
        print(traceback.format_exc())



def save_button2(message, table_data, table_producto, data_table, file_data, user_email): 
    if data_table is None or len(data_table) == 0:
        try:
            s3 = boto3.client('s3',
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_S3_REGION_NAME)
            
            for file in data_table:
                matching_files = [f for f in file_data if f['File Name'] == file['File Name']]
                if matching_files:
                    s3.put_object(Body=matching_files[0]['Content'],
                                  Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                  Key=f'uploaded_document_forms/{matching_files[0]["File Name"]}')
            
            message = dbc.Alert( [ html.I(className="bi bi-check-circle-fill me-2"), "Archivos cargados exitosamente", ], color="success", className="d-flex align-items-center", ),
            file_data.clear()
            send_email(user_email)
        except Exception as e:
            message = dbc.Alert( [ html.I(className="bi bi-x-octagon-fill me-2"), f'Error en cargar archivos: {str(e)}', ], color="danger", className="d-flex align-items-center", ),
    return [
        dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((
                html.Div(style={'height': '20px'}),
                html.Div(message, id='output-message', className="text-center"),
                html.Div(style={'height': '20px'}),
            ),width=10),
            dbc.Col((),width=1),
        ]),
        dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in pd.DataFrame(table_data).columns],
                data=table_data,
            )),width=10),
            dbc.Col((),width=1),
        ]),
        html.Div(style={'height': '40px'}),
        dbc.Row([
        dbc.Col((), width=1),
        dbc.Col((
            dash_table.DataTable(
                id='table_productos',
                columns=[{"name": i, "id": i} for i in pd.DataFrame(table_producto).columns],
                data=table_producto,
            )
        ), width=10),
        dbc.Col((), width=1),
    ]),
    html.Div(style={'height': '40px'}),
    dbc.Row([
        dbc.Col((), width=1),
        dbc.Col((
            dash_table.DataTable(
                id='data_table',
                columns=[{"name": i, "id": i} for i in pd.DataFrame(data_table).columns],
                data=data_table,
            )
        ), width=10),
        dbc.Col((), width=1),
    ]),
    html.Div(style={'height': '40px'}),
    ]



def message_alert(message_alert):
    print(message_alert),
    return[
            dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((
                html.Div(style={'height': '20px'}),
                dbc.Alert( [ html.I(className="bi bi-x-octagon-fill me-2"), message_alert, ], color="danger", className="d-flex align-items-center", ),
                html.Div(style={'height': '20px'}),
            ),width=10),
        ]),
        ]
