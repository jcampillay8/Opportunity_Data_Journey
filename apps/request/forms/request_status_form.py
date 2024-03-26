import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
from apps.request.models import CotizacionRealizada, CotizacionRealizada_Productos, CotizacionRealizada_Archivos, Estado_Solicitudes
import dash_daq as daq
from datetime import date
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
solicitud_revision_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud en Revisión').count()
solicitud_aprobada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Aprobada').count()
solicitud_finalizada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Finalizada').count()

# Use these counts in your figures
fig1 = go.Figure(go.Indicator(
    value = solicitud_creada_count,
    title = {"text": "Solicitud Creada"},
))

fig2 = go.Figure(go.Indicator(
    value = solicitud_revision_count,
    title = {"text": "Solicitud en Revisión"},
))

fig3 = go.Figure(go.Indicator(
    value = solicitud_aprobada_count,
    title = {"text": "Solicitud Aprobada"},
))

fig4 = go.Figure(go.Indicator(
    value = solicitud_finalizada_count,
    title = {"text": "Solicitud Finalizada"},
))

card1 = dbc.Card(
    dcc.Graph(figure=fig1, style={"height": "100%", "width": "100%"}),
    style={"height": "300px"}
)

card2 = dbc.Card(
    dcc.Graph(figure=fig2, style={"height": "100%", "width": "100%"}),
    style={"height": "300px"}
)

card3 = dbc.Card(
    dcc.Graph(figure=fig3, style={"height": "100%", "width": "100%"}),
    style={"height": "300px"}
)

card4 = dbc.Card(
    dcc.Graph(figure=fig4, style={"height": "100%", "width": "100%"}),
    style={"height": "300px"}
)



def serve_layout():  
    return dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(style={'height': '20px'}), width=12)
    ]),

    dbc.Row([dbc.Col(card1), dbc.Col(card2), dbc.Col(card3),dbc.Col(card4)]),

    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),
    html.Div(id='email', style={'display' : 'none'})    
    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout





