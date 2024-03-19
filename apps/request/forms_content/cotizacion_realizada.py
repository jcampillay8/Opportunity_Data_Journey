import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django.contrib.auth.models import User
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
import dash_daq as daq
from datetime import date
import dash_table
import pandas as pd
import os


# df_cotizacion_realizada = pd.DataFrame(columns=['User_Id', 'User_Name','Formulario', 'Nombre Proveedor', 'Rut_Proveedor', 'Empresa', 'Area', 'Centro Costo', 'Nombre Solicitante', 'Nombre de Quién Autoriza', 'Nombre Producto', 'Cantidad', 'Descripción Producto'])
df_cotizacion_realizada = pd.DataFrame(columns=['User_Id', 'User_Name','Formulario', 'Nombre Proveedor', 'Rut_Proveedor', 'Empresa', 'Area', 'Centro Costo', 'Nombre Solicitante', 'Nombre de Quién Autoriza'])
df_cotizacion_realizada_productos = pd.DataFrame(columns=['Nombre Producto', 'Cantidad', 'Descripción Producto'])

def form_cotizacion_realizada():
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
            ]), width=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_proveedor',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), width=9),
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
            ]), width=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_rut_proveedor',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), width=9),
                ])
            ),width=10),
            dbc.Col(width=1),

        ]),
    
        dbc.Row([    
        dbc.Col(width=1),
        dbc.Col((html.Div([
            html.Div(style={'height': '20px'}),  # Add a space
    
            html.Div(style={'height': 'form0px'}),  # Add a space
            dbc.Row([
                dbc.Col(dcc.Markdown(''' ### EMPRESA: '''), width=3),
                dbc.Col(dcc.Dropdown(id='empresa-dropdown', options=[{'label': i, 'value': i} for i in ['ETICSA', 'DTS']]), width=9),
            ]),
            html.Div(style={'height': '20px'}),  # Add a space between the dropdowns
            dbc.Row([
                dbc.Col(dcc.Markdown(''' ### ÁREA: '''), width=3),
                dbc.Col(dcc.Dropdown(id='area-dropdown'), width=9),
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
            ]), width=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_centro_costo',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), width=9),
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
            ]), width=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_solicitante',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), width=9),
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
            ]), width=3),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_autoriza',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), width=9),
                ])
            ),width=10),
            dbc.Col(width=1),

        ]),

        html.Div(style={'height': '40px'}),  # Add a space
                    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((
            dcc.Markdown(f''' ## DESGLOSE COMPRA ''', className="text-center"),
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
            ]), width=2),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_nombre_producto',
                    placeholder='Enter a value...',
                    type='text',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), width=6),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Markdown(''' ### CANTIDAD: '''),
            ]), width=2),
            dbc.Col(html.Div([
                html.Br(),
                dcc.Input(
                    id = 'input_cantidad',
                    placeholder='Enter a value...',
                    type='number',
                    value='',
                    style={'width': '100%'}
                ),
            ], className='pl-0'), width=2),
            
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
                columns=[{"name": i, "id": i} for i in df_cotizacion_realizada_productos.columns],
                data=df_cotizacion_realizada_productos.to_dict('records'),
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
            dcc.Markdown(f''' ## ADJUNTAR DOCUMENTOS (OPCIONAL) ''', className="text-center"),
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

def save_button2(message, table_data, table_producto, data_table, file_data):  # Agrega file_data como un argumento
    try:
        if not os.path.exists('uploaded_document_forms'):
            os.makedirs('uploaded_document_forms')
        for file in data_table:
            matching_files = [f for f in file_data if f['File Name'] == file['File Name']]
            if matching_files:
                with open(f'uploaded_document_forms/{matching_files[0]["File Name"]}', 'wb') as f:
                    f.write(matching_files[0]['Content'])
        message = 'Archivos cargados exitosamente'
    except Exception as e:
        message = f'Error en cargar archivos: {str(e)}'
    return [
        dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((
                html.Div(message, id='output-message')
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
    ])
    ]




