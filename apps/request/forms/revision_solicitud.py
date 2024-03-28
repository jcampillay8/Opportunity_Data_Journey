import dash
import dash_bootstrap_components as dbc
from dash import Dash, dash_table, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
from apps.request.models import CotizacionRealizada, CotizacionRealizada_Productos, CotizacionRealizada_Archivos, Estado_Solicitudes
from django.db.models import F
import dash_daq as daq
from datetime import date
from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required
import plotly.graph_objects as go
import requests

import base64
import datetime    
import io
import os

import pandas as pd

theme = dbc.themes.BOOTSTRAP

app = DjangoDash('Request_Revision_Solicitud_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP], meta_tags=[ { "name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1", }, ],)



def serve_layout():  
    return dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(style={'height': '40px'}), width=12)
    ]),
    dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
            dcc.Markdown('''# REVISIÓN SOLICITUD '''),

            ),width=10),
            dbc.Col(width=1),

        ]),
    dbc.Row([
        dbc.Col((html.Div(style={'height': '20px'})),width=1),
        dbc.Col((html.Div(id='output-user')),width=10),
        dbc.Col((html.Div(style={'height': '20px'})),width=1),
    ]),
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col((
        dbc.Row([
        dbc.Col(html.Div([
            html.Br(),
            dcc.Markdown(''' ### NOMBRE PRODUCTO: '''),
        ]), md=12, width=2, lg=2),
        dbc.Col(html.Div([
            html.Br(),
            dcc.Input(
                id = 'output_nombre_producto',
                placeholder='Enter a value...',
                type='text',
                value='',
                style={'width': '100%'},
                readOnly=True  # Make the input read-only
            ),
        ], className='pl-0'), md=12, width=6, lg=6),
        dbc.Col(html.Div([
            html.Br(),
            dcc.Markdown(''' ### CANTIDAD: '''),
        ]), md=12, width=2, lg=2),
        dbc.Col(html.Div([
            html.Br(),
            dcc.Input(
                id = 'output_cantidad',
                placeholder='Enter a value...',
                type='number',
                value='',
                style={'width': '100%'},
                readOnly=True  # Make the input read-only
            ),
        ], className='pl-0'), md=12, width=2, lg=2),
        
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
            id = 'output_descripcion_producto',
            placeholder='Describa el ítem...',
            style={'width': '100%'},
            readOnly=True  # Make the textarea read-only
        )
        ),width=10),
        dbc.Col(width=1),

    ]),
    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),

    # Add a Submit button to the layout
    html.Button('Submit', id='submit', n_clicks=0, style={'display': 'none'}),

    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout




@app.callback(
    Output('output-user', 'children'),
    [Input('submit', "n_clicks")],
    [State('user_id', 'children'),
     State('username', 'children'),
    ]
)
def get_user(n_clicks, user_id, username, request):  # Agrega pathname aquí
    user = request.user
    username = user.username
    user_id = user.id
    ID_OC = request.session.get('id')
    if n_clicks is not None:
        return f"El nombre de usuario es {username}, su id es {user_id} y el Id de OC es {ID_OC}"


# @app.callback(
#     [Output('output_nombre_producto', 'value'),
#      Output('output_cantidad', 'value'),
#      Output('output_descripcion_producto', 'value')],
#     [Input('submit', "n_clicks")],
# )
# def get_product(n_clicks,request):
#     ID_OC = request.session.get('id')
#     if n_clicks is not None:
#         product = CotizacionRealizada_Productos.objects.filter(ID_OC=ID_OC).first()
#         if product is not None:
#             return product.Nombre_Producto, product.Cantidad, product.Descripcion_Producto
#         else:
#             return "No se encontró un producto con ese id", "", ""
#     return "No se encontró un id válido", "", ""



@app.callback(
    [Output('output_nombre_producto', 'value'),
     Output('output_cantidad', 'value'),
     Output('output_descripcion_producto', 'value'),
     Output('output_nombre_producto', 'readOnly'),
     Output('output_cantidad', 'readOnly'),
     Output('output_descripcion_producto', 'readOnly')],
    [Input('submit', "n_clicks")],
)
def get_product(n_clicks,request):
    user = request.user
    id = request.session.get('id')  # Obtiene el id de la sesión
    user_id = user.id
    if n_clicks is not None:
        product = CotizacionRealizada_Productos.objects.filter(ID_OC_id=id).first()
        if user.is_superuser or user.is_staff:
            # Filtra por ID_OC_id en lugar de ID_OC
            if product is not None:
                return product.Nombre_Producto, product.Cantidad, product.Descripcion_Producto, False, False, False
            else:
                return "No se encontró un producto con ese id", "", "", True, True, True
        else:
            return product.Nombre_Producto, product.Cantidad, product.Descripcion_Producto, True, True, True
    return "No se encontró un id válido", "", "", True, True, True
