import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
import dash_daq as daq
from datetime import date
import dash_table
import pandas as pd

df_solicitud_cotizacion = pd.DataFrame(columns=['Nombre Proveedor', 'Empresa', 'Area'])

def form_solicitud_cotizacion(app, file_data):
    return[
    html.Br(),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((
            dcc.Markdown(f''' ## SOLICITUD DE COTIZACIÓN ''', className="text-center"),
        ),width=10),
        dbc.Col((),width=1),
    ]),
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
        html.Div(style={'height': '20px'}),  # Add a space
        dbc.Row([
        dbc.Col(width=4),
        dbc.Col(dbc.Button('SAVE DATA', id='save-button', n_clicks=0), width=4),
        dbc.Col(width=4),
    ]),

    ]),
    ]


def save_button(message, table_data):
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
                columns=[{"name": i, "id": i} for i in df_solicitud_cotizacion.columns],
                data=table_data,
            )),width=10),
            dbc.Col((),width=1),
        ])
    ]
