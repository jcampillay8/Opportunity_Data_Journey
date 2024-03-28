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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

theme = dbc.themes.BOOTSTRAP

app = DjangoDash('Request_Status_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP], meta_tags=[ { "name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1", }, ],)

# Count the number of rows for each status
solicitud_creada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Creada').count()


# Use these counts in your figures
fig1 = go.Figure(go.Indicator(
    value = solicitud_creada_count,
    title = {"text": "Solicitud Creada"},
))

card1 = dbc.Card(
    dcc.Graph(figure=fig1, style={"height": "100%", "width": "100%"}),
    style={"height": "300px"}
)

def serve_layout():  
    return dbc.Container([

    dbc.Row([
        dbc.Col((html.Div(style={'height': '20px'})),width=1),
        dbc.Col((dbc.Row([dbc.Col(card1)]),),width=10),
        dbc.Col((html.Div(style={'height': '20px'})),width=1),
    ]),

    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),

    # Add the 'output-user' to the layout
    html.Div(id='output-user'),

    # Add a Submit button to the layout
    html.Button('Submit', id='submit', n_clicks=0),

    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout


@app.callback(
    Output('output-user', 'children'),
    Input('submit', "n_clicks"),
    [State('user_id', 'children'),
     State('username', 'children')],
     prevent_initial_call=True,
)
def get_user(n_clicks, user_id, username,request):
    user = request.user
    username = user.username
    user_id = user.id
    if n_clicks is not None:
        return f"El nombre de usuario es {username} y su id es {user_id}"