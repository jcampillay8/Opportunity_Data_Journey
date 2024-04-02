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
from django.utils import timezone
import requests
from django.contrib import messages
import base64
import datetime    
import io
import os

import pandas as pd

theme = dbc.themes.BOOTSTRAP

app = DjangoDash('Request_Revision_Solicitud_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP])



def serve_layout():  
    return dbc.Container([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='REVISIÓN SOLICITUD', value='tab-1',children=[
            dbc.Row([
                dbc.Col(html.Div(style={'height': '40px'}), width=12)
            ]),
            dbc.Row([
                    dbc.Col(width=1),
                    dbc.Col((
                    dcc.Markdown('''# REVISIÓN SOLICITUD ''', className="text-center"),

                    ),width=10),
                    dbc.Col(width=1),
                ]),
            dbc.Row([
                dbc.Col(html.Div(style={'height': '20px'}), width=12)
            ]),
            dbc.Row([
                    dbc.Col(width=1),
                    dbc.Col((
                    html.Div(id='output_nombre_formulario', style={'fontSize': 30, 'font-weight': 'bold'}),
                    ),width=10),
                    dbc.Col(width=1),
                ]),
                            dbc.Row([
                    dbc.Col(width=1),
                    dbc.Col((
                    dbc.Row([
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Markdown(''' ### NÚMERO ORDEN COMPRA: '''),
                    ]), md=12, width=2, lg=2),
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Input(
                            id = 'input_numero_orden_compra',
                            placeholder='Enter a value...',
                            type='text',
                            value='',
                            style={'width': '100%'}
                        ),
                    ], className='pl-0'), md=12, width=4, lg=4),
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Markdown(''' ### NÚMERO FACTURA: '''),
                    ]), md=12, width=2, lg=2),
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Input(
                            id = 'input_numero_factura',
                            placeholder='Enter a value...',
                            type='text',
                            value='',
                            style={'width': '100%'}
                        ),
                    ], className='pl-0'), md=12, width=4, lg=4),
                    
                        ])
                    ),width=10),
                    dbc.Col(width=1),
                ]),

            dbc.Row([
                dbc.Col((html.Div(style={'height': '20px'})),width=1),
                dbc.Col((html.Div(id='output-user')),width=10),
                dbc.Col((html.Div(style={'height': '20px'})),width=1),
            ]),
            dbc.Row([
                dbc.Col(html.Div(style={'height': '20px'}), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.Div(style={'height': '20px'}), width=1),
                dbc.Col(html.Label("Seleccione Fila Para Editar", style={'fontSize': 24, 'font-weight': 'bold','color':'blue'}), width=10),
                dbc.Col(html.Div(style={'height': '20px'}), width=1),
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
                        editable=False,
                        row_selectable="single",
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                        },
                        style_data_conditional=[
                            {
                                'whiteSpace': 'normal',
                                'height': 'auto',   
                            },
                        ],
                        style_cell_conditional=[
                                                {
                                "if": {"state": "selected"},
                                "backgroundColor": "inherit !important",
                                "border": "inherit !important",
                            },
                            {
                                'if': {'column_id': 'Descripcion_Producto'},
                                'whiteSpace': 'normal',
                                'textAlign': 'left',
                                'height': 'auto',
                            },
                            {
                                'if': {'column_id': 'Nombre_Producto'},
                                'textAlign': 'center',
                                'height': 'auto',
                            },
                            {
                                'if': {'column_id': 'Cantidad'},
                                'textAlign': 'center',
                                'height': 'auto',
                            }
                        ],
                    )
                ),width=10),
                dbc.Col(width=1),
            ]),
            dbc.Row([
                    dbc.Col((html.Div(style={'height': '40px'})),width=1),
                ]),
            dbc.Row([
                dbc.Col(width=2),
                dbc.Col(dbc.Button('ACTUALIZAR DATOS FILA', id='update-button', style={'display': 'none'}), width=8),
                dbc.Col(width=2),
            ]),
            dbc.Row([
                    dbc.Col((),width=1),
                    dbc.Col((
                        html.Div(style={'height': '20px'}),
                        html.Div( id='output-message', className="text-center"),
                        html.Div(style={'height': '20px'}),
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
                        ]), md=12, width=2, lg=2),
                        dbc.Col(html.Div([
                            html.Br(),
                            dcc.Input(
                                id='input_nombre_producto',
                                placeholder='Enter a value...',
                                type='text',
                                value='',
                                readOnly=True,
                                style={'width': '100%'}
                            ),
                        ], className='pl-0'), md=12, width=6, lg=6),
                        dbc.Col(html.Div([
                            html.Br(),
                            dcc.Markdown(''' ### CANTIDAD: '''),
                        ]), md=12, width=2, lg=2),
                        dbc.Col(html.Div([
                            html.Br(),
                            dcc.Input(
                                id='input_cantidad',
                                placeholder='Enter a value...',
                                type='number',
                                value='',
                                readOnly=True,
                                style={'width': '100%'}
                            ),
                        ], className='pl-0'), md=12, width=2, lg=2),
                    ])
                ), width=10),
                dbc.Col(width=1),
            ]),
            html.Div(style={'height': '40px'}),
            dbc.Row([
                dbc.Col(width=1),
                dbc.Col((
                    dcc.Markdown(''' ### DESCRIPCIÓN PRODUCTO: '''),
                ), width=10),
                dbc.Col(width=1),
            ]),
            dbc.Row([
                dbc.Col(width=1),
                dbc.Col((
                    dcc.Textarea(
                        id='input_descripcion_producto',
                        placeholder='Describa el ítem...',
                        readOnly=True,
                        style={'width': '100%'}
                    )
                ), width=10),
                dbc.Col(width=1),
            ]),
            html.Div(style={'height': '40px'}),
            dbc.Row([
                dbc.Col(width=2),
                dbc.Col(dbc.Button('SOLICITUD AJUSTE INFORMACIÓN', id='ajuste-button', style={'display': 'block', 'background-color':'#FFD700', 'color': 'black'}), width=4),
                dbc.Col(dbc.Button('GUARDAR & APROBAR', id='save-button', style={'display': 'none'}), width=4),
                dbc.Col(width=2),
            ]),
        ]),
        dcc.Tab(label='SOLICITUD AJUSTE INFORMACIÓN', id='Tab-2', value='tab-2', children=[
            dbc.Row([
                dbc.Col(html.Div(style={'height': '40px'}), width=12)
            ]),
            dbc.Row([
                dbc.Col((),width=1),
                dbc.Col((dcc.Markdown('''# AJUSTE INFORMACIÓN ''', className="text-center")),width=10),
                dbc.Col((),width=1),
            ]),
            dbc.Row([
                dbc.Col(html.Div(style={'height': '20px'}), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.Div(style={'height': '20px'}), width=1),
                dbc.Col(html.Label("Ingrese Informaicón a ser Ajustada", style={'fontSize': 24, 'font-weight': 'bold','color':'blue'}), width=10),
                dbc.Col(html.Div(style={'height': '20px'}), width=1),
            ]),
            dbc.Row([
                dbc.Col((),width=1),
                dbc.Col((
                dcc.Textarea(
                    id='input_texto_ajuste_informacion',
                    placeholder='Describa el ítem...',
                    readOnly=False,
                    style={'width': '100%'}
                )
                ), width=10),
                dbc.Col((),width=1),
            ]),
            dbc.Row([
                dbc.Col(html.Div(style={'height': '20px'}), width=12)
            ]),
            dbc.Row([
                    dbc.Col((),width=1),
                    dbc.Col((
                        html.Div(style={'height': '20px'}),
                        html.Div( id='output-message_ajuste', className="text-center"),
                        html.Div(style={'height': '20px'}),
                    ),width=10),
                    dbc.Col((),width=1),
                ]),
    dbc.Row([
        dbc.Col(width=2),
        dbc.Col(dbc.Button('ENVIAR AJUSTE INFORMACIÓN', id='enviar-ajuste-button', style={'display': 'block', 'background-color':'#FFD700', 'color': 'black'}), width=4),
        dbc.Col(width=2),
    ]),
        ]),
    ],style={ 'background': '#0074D9','color':'black', 'fontSize': 30, 'font-weight': 'bold'}),
    html.Div(id='tabs-content-props'),

    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),
    dcc.ConfirmDialog(id='confirm',message=''),
    dcc.ConfirmDialog(id='confirm_ajuste',message=''),

    # Add a Submit button to the layout
    html.Button('Submit', id='submit', n_clicks=0, style={'display': 'none'}),

    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout


@app.callback(
    [Output('save-button', 'style'),
     Output('update-button', 'style'),
     Output('input_numero_orden_compra', 'readOnly'),
     Output('input_numero_factura', 'readOnly',
     )],
    [Input('submit', "n_clicks")],
)
def update_buttons(n_clicks, request):
    user = request.user
    if n_clicks is not None:
        if user.is_superuser or user.is_staff:
            return {'display': 'block'}, {'display': 'block'}, False, False
        else:
            return {'display': 'none'}, {'display': 'none'}, True, True
    return {'display': 'none'}, {'display': 'none'}, True, True



@app.callback(
    [Output('input_nombre_producto', 'value'),
     Output('input_nombre_producto', 'readOnly'),
     Output('input_cantidad', 'value'),
     Output('input_cantidad', 'readOnly'),
     Output('input_descripcion_producto', 'value'),
     Output('input_descripcion_producto', 'readOnly')],
    [Input('output-table', 'selected_rows'),
     Input('output-table', 'data')]
)
def update_output(selected_rows, data,request):
    user = request.user
    if selected_rows:
        selected_row_data = data[selected_rows[0]]
        if user.is_superuser or user.is_staff:
            return selected_row_data['Nombre_Producto'], False, selected_row_data['Cantidad'], False, selected_row_data['Descripcion_Producto'], False
        else:
            return selected_row_data['Nombre_Producto'], True, selected_row_data['Cantidad'], True, selected_row_data['Descripcion_Producto'], True
    else:
        return "", True, "", True, "", True



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
    [Output('output_nombre_formulario','children'),
     Output('output-table', 'data'),
     Output('output-table', 'editable')],
    [Input('submit', "n_clicks"),
     Input('update-button', 'n_clicks')],
    [State('output-table', 'selected_rows'),
     State('output-table', 'data'),
     State('input_nombre_producto', 'value'),
     State('input_cantidad', 'value'),
     State('input_descripcion_producto', 'value')]
)
def update_output(n_clicks_submit, n_clicks_update, selected_rows, data, nombre_producto, cantidad, descripcion_producto,request):


    user = request.user
    id = request.session.get('id')  # Obtiene el id de la sesión
    user_id = user.id

    if n_clicks_update is not None and selected_rows:
        data[selected_rows[0]]['Nombre_Producto'] = nombre_producto
        data[selected_rows[0]]['Cantidad'] = cantidad
        data[selected_rows[0]]['Descripcion_Producto'] = descripcion_producto
        return dash.no_update, data, dash.no_update
    
    elif n_clicks_submit is not None:
        data_cotizacion = CotizacionRealizada.objects.filter(id=id).first()
        nombre_formulario = data_cotizacion.Formulario
        data_formulario = nombre_formulario + '  ID: '+str(id)
        products = CotizacionRealizada_Productos.objects.filter(ID_OC_id=id)  # Obtiene todos los productos
        # Crea una lista de diccionarios con los datos de los productos
        data = [{'ID': product.id, 'Nombre_Producto': product.Nombre_Producto, 'Cantidad': product.Cantidad, 'Descripcion_Producto': product.Descripcion_Producto} for product in products]
        if user.is_superuser or user.is_staff:
            return data_formulario, data, False
        else:
            return data_formulario, data, False

    return "", [], False




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
    [State('output-table', 'data'),
    State('input_numero_orden_compra', 'value'),
    State('input_numero_factura', 'value')]
)
def update_output(submit_n_clicks, table_data,numero_orden_compra, numero_factura,  request):
    id = request.session.get('id')
    if submit_n_clicks is not None:
        try:
            CotizacionRealizada.objects.filter(id=id).update(
                Numero_Orden_compra=numero_orden_compra,
                Numero_Factura=numero_factura
            )
            # Itera sobre cada fila en los datos de la tabla
            for row in table_data:
                # Actualiza los datos en la base de datos para cada producto
                CotizacionRealizada_Productos.objects.filter(ID_OC_id=id, id=row['ID']).update(
                    Nombre_Producto=row['Nombre_Producto'],
                    Cantidad=row['Cantidad'],
                    Descripcion_Producto=row['Descripcion_Producto']
                )

              
            # Obtén el objeto Estado_Solicitudes correspondiente
            estado_solicitud = Estado_Solicitudes.objects.get(ID_OC=id)
            
            # Si el estado actual no es "Solicitud en Revisión", actualiza el estado
            if estado_solicitud.Request_Status == "Solicitud en Revisión" or estado_solicitud.Request_Status == "Solicitud Ajuste Información" :
                estado_solicitud.Request_Status = "Solicitud Aprobada"
                estado_solicitud.Solicitud_Ajuste_Informacion = True
                estado_solicitud.Solicitud_Aprobada = True
                estado_solicitud.Hora_Inicio_Aprobada = timezone.now()
                estado_solicitud.save()

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

@app.callback(
    Output('tabs-styled-with-props', 'value'),  # Actualiza el valor de 'tabs-example'
    [Input('ajuste-button', 'n_clicks')],
    prevent_initial_call=True
)
def change_tab(n_clicks):
    if n_clicks is not None:  # Si el botón ha sido presionado
        return 'tab-2'


@app.callback(
    [Output("confirm_ajuste", "displayed"), Output("confirm_ajuste", "message"), Output("enviar-ajuste-button", "style")],
    [Input("enviar-ajuste-button", "n_clicks")],
    prevent_initial_call=True
)
def open_confirm_dialog(n_clicks, request):
    user = request.user
    if user.is_superuser or user.is_staff:
        if n_clicks is not None and n_clicks > 0:
            return True, "¿Está seguro de enviar ajuste de información?", {'display': 'block', 'background-color':'#FFD700', 'color': 'black'}
        return False, "", {'display': 'block', 'background-color':'#FFD700', 'color': 'black'},
    else:
        return False, "", {'display': 'none'}


@app.callback(
    Output('output-message_ajuste', 'children'),
    [Input('confirm_ajuste', 'submit_n_clicks')],
    [State('input_texto_ajuste_informacion', 'value')]
)
def update_output2(submit_n_clicks, texto_ajuste,  request):
    id = request.session.get('id')
    
    if submit_n_clicks is not None:
        try:
            CotizacionRealizada.objects.filter(id=id).update(
                texto_ajuste_informacion_solicitud=texto_ajuste
            )

            # Obtén el objeto Estado_Solicitudes correspondiente
            estado_solicitud = Estado_Solicitudes.objects.get(ID_OC=id)
            
            # Si el estado actual no es "Solicitud Ajuste Información", actualiza el estado
            if estado_solicitud.Request_Status != "Solicitud Ajuste Información":
                estado_solicitud.Request_Status = "Solicitud Ajuste Información"
                estado_solicitud.Solicitud_Ajuste_Informacion = True
                estado_solicitud.Hora_Inicio_Solicitud_Ajuste_Informacion = timezone.now()
                estado_solicitud.save()

            # Si la actualización fue exitosa, devuelve un mensaje de éxito
            return dbc.Alert(
                [html.I(className="bi bi-check-circle-fill me-2"), "Solicitud Ajuste Informaición enviado exitosamente"],
                color="success",
                className="d-flex align-items-center",
            )
        except Exception as e:
            # Si ocurrió un error durante la actualización, devuelve un mensaje de error
            return dbc.Alert(
                [html.I(className="bi bi-x-octagon-fill me-2"), f'Error actualización ajuste información: {str(e)}'],
                color="danger",
                className="d-flex align-items-center",
            )
    # Si el usuario hizo clic en "Cancelar", no devuelve nada
    return None