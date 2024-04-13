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
import base64
import datetime    
import io
import os

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

theme = dbc.themes.BOOTSTRAP

#app = DjangoDash('Request_Status_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP], meta_tags=[ { "name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1" } ],)
app = DjangoDash('Request_Status_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP])


# Update the serve_layout function to include the 'output-card' in the layout
def serve_layout():  
    return dbc.Container([
    dcc.Location(id='url', refresh=True),
    dbc.Row([
        dbc.Col(html.Div(style={'height': '20px'}), width=12)
    ]),

dbc.Row([
    dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
    dbc.Col((dbc.Row([
        dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
        dbc.Col((html.Div(id='output-card1')),md=12, lg=2),
        dbc.Col((html.Div(id='output-card2')),md=12, lg=2),
        dbc.Col((html.Div(id='output-card3')),md=12, lg=2),
        dbc.Col((html.Div(id='output-card4')),md=12, lg=2),
        dbc.Col((html.Div(id='output-card5')),md=12, lg=2),
        dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
    ])),md=12, lg=12),
    dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
]),

    dbc.Row([
        dbc.Col(html.Div(style={'height': '40px'}), width=12)
    ]),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((dash_table.DataTable(

        id='datatable-interactivity',
        columns=[
            {"name": "ID_OC_id", "id": "ID_OC_id", "deletable": True, "selectable": True,'type': 'numeric'},
            {"name": "Request_Status", "id": "Request_Status", "deletable": True, "selectable": True},
            {"name": "User_Id", "id": "User_Id", "deletable": True, "selectable": True,'type': 'numeric'},
            {"name": "User_Name", "id": "User_Name", "deletable": True, "selectable": True},
            {"name": "Formulario", "id": "Formulario", "deletable": True, "selectable": True},
            {"name": "Empresa", "id": "Empresa", "deletable": True, "selectable": True},
            {"name": "Area", "id": "Area", "deletable": True, "selectable": True},
            {"name": "Centro_Costo", "id": "Centro_Costo", "deletable": True, "selectable": True},
            {"name": "Nombre_Solicitante", "id": "Nombre_Solicitante", "deletable": True, "selectable": True},
            {"name": "Nombre_Autoriza", "id": "Nombre_Autoriza", "deletable": True, "selectable": True},
            {"name": "hora_solicitud", "id": "hora_solicitud", "deletable": True, "selectable": True},
            {"name": "fecha_solicitud", "id": "fecha_solicitud", "deletable": True, "selectable": True},
        ],
            data=[],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="single",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_cell_conditional=[
               {
                "if": {"state": "selected"},
                "backgroundColor": "inherit !important",
                "border": "inherit !important",
               }
            ],
            style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'textAlign': 'center',
                    'fontWeight': '450',
                    'font-family': 'Courier',
                },
            style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'font-family': 'Courier',
            },
        )),width=10),
        dbc.Col(html.Div(style={'height': '20px'}),width=1),
    ]),
    
    dbc.Row([
        dbc.Col(html.Div(style={'height': '20px'}), width=12)
    ]),

    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),

    # Add a Submit button to the layout
    html.Button('Submit', id='submit', n_clicks=0, style={'display': 'none'}),

    dbc.Row([
        dbc.Col((),width=2),
        dbc.Col((dbc.Button('Watch', id='watch-button', n_clicks=0)),width=9),
        dbc.Col((),width=1),
    ]),


    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout

@app.callback(
    Output('url', 'pathname'),
    Input('watch-button', 'n_clicks'),
    State('datatable-interactivity', 'derived_virtual_selected_rows'),
    State('datatable-interactivity', 'data'),
    prevent_initial_call=True,
)
def watch_button(n_clicks, derived_virtual_selected_rows, data, request):
    user = request.user
    if n_clicks > 0:
        if user.is_superuser or user.is_staff:
            if len(derived_virtual_selected_rows) == 1:
                dff = pd.DataFrame(data)
                selected_row_id = dff.iloc[derived_virtual_selected_rows[0]]['ID_OC_id']
                
                # Obtén el objeto Estado_Solicitudes correspondiente
                estado_solicitud = Estado_Solicitudes.objects.get(ID_OC=selected_row_id)
                
                # Si el estado actual no es "Solicitud en Revisión", actualiza el estado
                if estado_solicitud.Request_Status == "Solicitud Creada":
                    estado_solicitud.Request_Status = "Solicitud en Revisión"
                    estado_solicitud.Solicitud_Revision = True
                    estado_solicitud.Hora_Inicio_Solicitud_Revision = timezone.now()
                    estado_solicitud.save()
                
                return '/request/revision_solicitud/{}'.format(selected_row_id)
        else:
            if len(derived_virtual_selected_rows) == 1:
                dff = pd.DataFrame(data)
                selected_row_id = dff.iloc[derived_virtual_selected_rows[0]]['ID_OC_id']
                return '/request/revision_solicitud/{}'.format(selected_row_id)
    return dash.no_update

@app.callback(
    Output('output-card1', 'children'),
    Output('output-card2', 'children'),
    Output('output-card3', 'children'),
    Output('output-card4', 'children'),
    Output('output-card5', 'children'),
    Output('datatable-interactivity', 'data'),
    Input('submit', "n_clicks"),
    [State('user_id', 'children'),
     State('username', 'children')],
     
)
def get_user(n_clicks, user_id, username, request):
    user = request.user
    username = user.username
    user_id = user.id
    if n_clicks is not None:
        if user.is_superuser or user.is_staff:
            solicitud_creada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Creada').count()
            solicitud_revision_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud en Revisión').count()
            solicitud_ajuste_informacion_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Ajuste Información').count()
            solicitud_aprobada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Aprobada').count()
            solicitud_finalizada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Finalizada').count()
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
        else:
            solicitud_creada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Creada', ID_OC__User_Id=user_id).count()
            solicitud_revision_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud en Revisión', ID_OC__User_Id=user_id).count()
            solicitud_ajuste_informacion_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Ajuste Información', ID_OC__User_Id=user_id).count()
            solicitud_aprobada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Aprobada', ID_OC__User_Id=user_id).count()
            solicitud_finalizada_count = Estado_Solicitudes.objects.filter(Request_Status='Solicitud Finalizada', ID_OC__User_Id=user_id).count()
            qs = Estado_Solicitudes.objects.filter(ID_OC__User_Id=user_id).select_related('ID_OC').values(
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
            # Formatea las columnas 'hora_solicitud' y 'fecha_solicitud'
        df['ID_OC_id'] = pd.to_numeric(df['ID_OC_id'])
        df['User_Id'] = pd.to_numeric(df['User_Id'])
        df['hora_solicitud'] = df['hora_solicitud'].dt.strftime('%H:%M:%S')
        df['fecha_solicitud'] = df['fecha_solicitud'].dt.strftime('%d-%m-%Y')

        fig1 = go.Figure(go.Indicator(
            value = solicitud_creada_count,
            title = {"text": "Solicitud<br>Creada"},
        ))

        fig2 = go.Figure(go.Indicator(
            value = solicitud_revision_count,
            title = {"text": "Solicitud en<br>Revisión"},
        ))

        fig3 = go.Figure(go.Indicator(
            value = solicitud_ajuste_informacion_count,
            title = {"text": "Solicitud Ajuste<br>Información"},
        ))

        fig4 = go.Figure(go.Indicator(
            value = solicitud_aprobada_count,
            title = {"text": "Solicitud<br>Aprobada"},
        ))

        fig5 = go.Figure(go.Indicator(
            value = solicitud_finalizada_count,
            title = {"text": "Solicitud<br>Finalizada"},
        ))

        card1 = dbc.Card(
            dcc.Graph(figure=fig1, style={"height": "100%", "width": "100%"}),
            style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
        )

        card2 = dbc.Card(
            dcc.Graph(figure=fig2, style={"height": "100%", "width": "100%"}),
            style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
        )

        card3 = dbc.Card(
            dcc.Graph(figure=fig3, style={"height": "100%", "width": "100%"}),
            style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
        )

        card4 = dbc.Card(
            dcc.Graph(figure=fig4, style={"height": "100%", "width": "100%"}),
            style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
        )

        card5 = dbc.Card(
            dcc.Graph(figure=fig5, style={"height": "100%", "width": "100%"}),
            style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
        )


        return card1, card2, card3, card4, card5, df.to_dict('records')