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
import plotly.express as px
import pandas as pd

theme = dbc.themes.BOOTSTRAP


<<<<<<< HEAD
# Obtén todos los objetos CotizacionRealizada
cotizaciones = CotizacionRealizada.objects.values()

# Convierte los datos a DataFrame
df_data_solicitudes = pd.DataFrame.from_records(cotizaciones)


app = DjangoDash('Request_Histogram_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP])

=======
app = DjangoDash('Request_Histogram_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP])
>>>>>>> stage

def update_data():
    cotizaciones = CotizacionRealizada.objects.values()
    df_data_solicitudes = pd.DataFrame.from_records(cotizaciones)
    return df_data_solicitudes

def serve_layout():
    df_data_solicitudes = update_data()
    return dbc.Container([
        dbc.Row([
                dbc.Col(html.Div(style={'height': '60px'}), width=12)
            ]),
        dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((
                html.H2("Nombre_Proveedor Count Bar Chart"),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=df_data_solicitudes['fecha_solicitud'].min(),
                    end_date=df_data_solicitudes['fecha_solicitud'].max()
                ),  
                dcc.Graph(id='graph3'),
            ),width=10),
            dbc.Col((),width=1),
        ]),
        dbc.Row([
                dbc.Col(html.Div(style={'height': '60px'}), width=12)
            ]),
        dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((
                html.H2("Formulario and Empresa Histogram"),
                dcc.Dropdown(
                    id='dropdown2',
                    options=[{'label': str((i,j)), 'value': str((i,j))} for i,j in df_data_solicitudes[['Formulario', 'Empresa']].drop_duplicates().values],
                    value=[str((i,j)) for i,j in df_data_solicitudes[['Formulario', 'Empresa']].drop_duplicates().values],
                    multi=True
                ),
                dcc.Graph(id='graph2'),),width=10),
            dbc.Col((),width=1),
        ]),
        dbc.Row([
                dbc.Col(html.Div(style={'height': '60px'}), width=12)
            ]),
        dbc.Row([
            dbc.Col((),width=1),
            dbc.Col(( 
                html.H2("Nombre_Proveedor Histogram"),
                dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in df_data_solicitudes['Nombre_Proveedor'].unique()],
                    value=df_data_solicitudes['Nombre_Proveedor'].unique(),
                    multi=True),
                
                dcc.Graph(id='graph'),),width=10),
            dbc.Col((),width=1),
        ]),

    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),
    dcc.ConfirmDialog(id='confirm',message=''),
    dcc.ConfirmDialog(id='confirm_ajuste',message=''),

    html.Button('Submit', id='submit', n_clicks=0, style={'display': 'none'}),
    ],
    fluid=True,
    style={'padding-bottom':'200px'},
    )

app.layout = serve_layout




@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_dropdown_value):
    df_data_solicitudes = update_data()
    if type(selected_dropdown_value) == str:
        selected_dropdown_value = [selected_dropdown_value]
    filtered_df = df_data_solicitudes[df_data_solicitudes['Nombre_Proveedor'].isin(selected_dropdown_value)]
    fig = px.histogram(filtered_df, x='fecha_solicitud', color='Nombre_Proveedor', nbins=50)
    fig.update_traces(marker_line_width=1, marker_line_color='black')
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(tickangle=90)
    return fig

@app.callback(
    Output('graph2', 'figure'),
    [Input('dropdown2', 'value')]
)
def update_graph2(selected_dropdown_value):
    df_data_solicitudes = update_data()
    if type(selected_dropdown_value[0]) == str:
        selected_dropdown_value = [eval(i) for i in selected_dropdown_value]
    filtered_df = df_data_solicitudes[df_data_solicitudes[['Formulario', 'Empresa']].apply(tuple, axis=1).isin(selected_dropdown_value)]
    fig = px.histogram(filtered_df, x='fecha_solicitud', color='Empresa', facet_row='Formulario', nbins=50)
    fig.update_traces(marker_line_width=1, marker_line_color='black')
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(tickangle=90)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig

@app.callback(
    Output('graph3', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph3(start_date, end_date):
    df_data_solicitudes = update_data()
    filtered_df = df_data_solicitudes[(df_data_solicitudes['fecha_solicitud'] >= start_date) & (df_data_solicitudes['fecha_solicitud'] <= end_date)]
    count_df = filtered_df['Nombre_Proveedor'].value_counts().reset_index()
    count_df.columns = ['Nombre_Proveedor', 'count']
    fig = px.bar(count_df, x='Nombre_Proveedor', y='count')
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(tickangle=90)
    return fig