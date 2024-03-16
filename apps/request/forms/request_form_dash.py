import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
import dash_daq as daq
from datetime import date
from apps.request.forms_content.cotizacion_realizada import form_cotizacion_realizada
from apps.request.forms_content.solicitud_cotizacion import form_solicitud_cotizacion


theme = dbc.themes.BOOTSTRAP

app = DjangoDash('Request_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP], meta_tags = None)



def serve_layout():  
    return dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(style={'height': '20px'}), width=12)
    ]),
    
    dbc.Row([    
        dbc.Col(width=2),
        dbc.Col((html.Div([
            html.Div(style={'height': '20px'}),  # Add a space
            dcc.Markdown(''' # SELECCIONE \'SOLICITUD FORMULARIO\' '''),
            html.Div(style={'height': '40px'}),  # Add a space
            dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i} for i in ['Cotización Realizada', 'Solicitud de Cotización']],),
            html.Br(),
            dbc.Button('Submit', id='submit-button', n_clicks=0),
            ])),width=8),
        dbc.Col(width=2)
    ]),
    
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(html.Div(id='output-container'), width=10),
        dbc.Col(width=1),
    ]),
        
    ],
    fluid=True,
)

app.layout = serve_layout


@app.callback(
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('dropdown', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        if value == 'Cotización Realizada':
            return form_cotizacion_realizada()
        elif value == 'Solicitud de Cotización':
            return form_solicitud_cotizacion()
    else:
        return []



