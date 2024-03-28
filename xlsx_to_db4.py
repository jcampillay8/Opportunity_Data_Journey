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

qs = Estado_Solicitudes.objects.select_related('ID_OC').values(
    "ID_OC_id",
    "Request_Status",
    User_Id=F('ID_OC__User_Id'),
    User_Name=F('ID_OC__User_Name'),
    Formulario=F('ID_OC__Formulario'),
    Empresa=F('ID_OC__Empresa'),
    Area=F('ID_OC__Area'),
    Centro_Costo=F('ID_OC__Centro_Costo'),
    Nombre_Solicitante=F('ID_OC__Nombre_Solicitante'),
    Nombre_Autoriza=F('ID_OC__Nombre_Autoriza'),
    hora_solicitud=F('ID_OC__hora_solicitud'),
    fecha_solicitud=F('ID_OC__fecha_solicitud')
).order_by('-fecha_solicitud', '-hora_solicitud')

df = pd.DataFrame.from_records(qs)

def serve_layout():  
    return dbc.Container([
    dcc.Location(id='url', refresh=True),  # Agrega esto a tu layout
    dbc.Row([
        dbc.Col(html.Div(style={'height': '40px'}), width=12)
    ]),
    dbc.Row([
        dbc.Col((html.Div(style={'height': '20px'})),width=1),
        dbc.Col((dbc.Row([dbc.Col(card1), dbc.Col(card2), dbc.Col(card3),dbc.Col(card4)]),),width=10),
        dbc.Col((html.Div(style={'height': '20px'})),width=1),
    ]),
    dbc.Row([
        dbc.Col(html.Div(style={'height': '40px'}), width=12)
    ]),
        dbc.Row([
        dbc.Col((html.Div(style={'height': '20px'})),width=1),
        dbc.Col((    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="single",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    dbc.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='datatable-interactivity-container')),width=10),
    dbc.Col((html.Div(style={'height': '20px'})),width=1),
    ]),
    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),
    html.Div(id='email', style={'display' : 'none'})  
         


    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout

@callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    [Output('url', 'pathname'), Output('datatable-interactivity-container', "children")],
    Input('submit-button', 'n_clicks'),
    State('datatable-interactivity', "derived_virtual_data"),
    State('datatable-interactivity', "derived_virtual_selected_rows"),
    prevent_initial_call=True)
def update_graphs(n_clicks, rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    if len(derived_virtual_selected_rows) > 1:
        return dash.no_update, html.Div([
            'El valor de la primera columna de las filas seleccionadas es: {}'.format(', '.join([str(dff.iloc[i, 0]) for i in derived_virtual_selected_rows]))
        ])
    elif len(derived_virtual_selected_rows) == 1:
        selected_row_id = dff.iloc[derived_virtual_selected_rows[0]]['ID_OC_id']
        return '/request/revision_solicitud/{}'.format(selected_row_id), dash.no_update
    else:
        return dash.no_update, html.Div([])






