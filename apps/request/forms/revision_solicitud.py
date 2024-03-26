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
            dcc.Markdown(id='values'),

            ),width=10),
            dbc.Col(width=1),

        ]),

    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout



@app.callback(
    Output('values', 'children'),
    [Input('url', 'pathname')])
def update_values(pathname):
    
    if pathname.startswith('/revision_solicitud/'):
        values = pathname.split('request/revision_solicitud/')[1]
        
        return dcc.Markdown('''*** VALUES *** \n\n{}'''.format(values))
    else:
        return ''

