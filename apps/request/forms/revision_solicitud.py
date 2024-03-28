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
from django.contrib import messages
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
            dbc.Col(width=1),
            dbc.Col((
            html.Div(id='output_nombre_formulario', style={'fontSize': 30, 'font-weight': 'bold'}),
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
            dash_table.DataTable(
                id='output-table',
                columns=[
                    {"name": "ID", "id": "ID"},
                    {"name": "Nombre Producto", "id": "Nombre_Producto"},
                    {"name": "Cantidad", "id": "Cantidad"},
                    {"name": "Descripción Producto", "id": "Descripcion_Producto"}
                ],
                data=[],
                editable=True,  # Hace que la tabla sea editable
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ),width=10),
        dbc.Col(width=1),
    ]),
    dbc.Row([  # Agrega esta línea
        dbc.Col(width=1),
        dbc.Col((dbc.Button('SAVE', id='save-button', style={'display': 'none'})),width=10),  # Agrega esta línea
        dbc.Col(width=1),
    ]),  # Agrega esta línea
    dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((
                html.Div(style={'height': '20px'}),
                html.Div( id='output-message', className="text-center"),
                html.Div(style={'height': '20px'}),
            ),width=10),
            dbc.Col((),width=1),
        ]),
    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),
    dcc.ConfirmDialog(id='confirm',message=''),

    # Add a Submit button to the layout
    html.Button('Submit', id='submit', n_clicks=0, style={'display': 'none'}),

    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout


@app.callback(
    Output('save-button', 'style'),
    [Input('submit', "n_clicks")],
)
def update_button(n_clicks, request):
    user = request.user
    if n_clicks is not None:
        if user.is_superuser or user.is_staff:
            return {'display': 'block'}
        else:
            return {'display': 'none'}
    return {'display': 'none'}


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


@app.callback(
    [Output('output-table', 'data'),
     Output('output-table', 'editable')],
    [Input('submit', "n_clicks")],
)
def get_product(n_clicks,request):
    user = request.user
    id = request.session.get('id')  # Obtiene el id de la sesión
    user_id = user.id
    if n_clicks is not None:
        products = CotizacionRealizada_Productos.objects.filter(ID_OC_id=id)  # Obtiene todos los productos
        # Crea una lista de diccionarios con los datos de los productos
        data = [{'ID': product.id, 'Nombre_Producto': product.Nombre_Producto, 'Cantidad': product.Cantidad, 'Descripcion_Producto': product.Descripcion_Producto} for product in products]
        if user.is_superuser or user.is_staff:
            return data, True
        else:
            return data, False
    return [], False




@app.callback(
    [Output("confirm", "displayed"), Output("confirm", "message")],
    [Input("save-button", "n_clicks")]
)
def open_confirm_dialog(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return True, "¿Está seguro de guardar la información?"
    return False, ""



@app.callback(
    Output('output-message', 'children'),
    [Input('confirm', 'submit_n_clicks')],
    [State('output-table', 'data')]
)
def update_output(submit_n_clicks, table_data, request):
    id = request.session.get('id')
    if submit_n_clicks is not None:
        try:
            # Itera sobre cada fila en los datos de la tabla
            for row in table_data:
                # Actualiza los datos en la base de datos para cada producto
                CotizacionRealizada_Productos.objects.filter(ID_OC_id=id, id=row['ID']).update(
                    Nombre_Producto=row['Nombre_Producto'],
                    Cantidad=row['Cantidad'],
                    Descripcion_Producto=row['Descripcion_Producto']
                )

            # Si la actualización fue exitosa, devuelve un mensaje de éxito
            return dbc.Alert(
                [html.I(className="bi bi-check-circle-fill me-2"), "Datos actualizados exitosamente"],
                color="success",
                className="d-flex align-items-center",
            )
        except Exception as e:
            # Si ocurrió un error durante la actualización, devuelve un mensaje de error
            return dbc.Alert(
                [html.I(className="bi bi-x-octagon-fill me-2"), f'Error actualización datos: {str(e)}'],
                color="danger",
                className="d-flex align-items-center",
            )
    # Si el usuario hizo clic en "Cancelar", no devuelve nada
    return None

