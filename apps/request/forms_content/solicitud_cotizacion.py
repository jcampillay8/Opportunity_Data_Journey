import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
import dash_daq as daq
from datetime import date

def form_solicitud_cotizacion():
    return[
    html.Br(),
    dcc.Markdown(f''' ## SOLICITUD DE COTIZACIÓN '''),
    # dbc.Row([
    #     dbc.Row([
    #         dbc.Col(width=1),
    #         dbc.Col((
    #             dbc.Row([
    #                             dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Markdown(''' ### NOMBRE: '''),
    #         ]), width=3),
    #         dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Input(
    #                 placeholder='Enter a value...',
    #                 type='text',
    #                 value='',
    #                 style={'width': '100%'}
    #             ),
    #         ], className='pl-0'), width=9),
    #             ])
    #         ),width=10),
    #         dbc.Col(width=1),
    #     ]),
    #     dbc.Row([
    #         dbc.Col(width=1),
    #         dbc.Col((
    #             dbc.Row([
    #                             dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Markdown(''' ### RUT PROVEEDOR: '''),
    #         ]), width=3),
    #         dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Input(
    #                 placeholder='Enter a value...',
    #                 type='number',
    #                 value='',
    #                 style={'width': '100%'}
    #             ),
    #         ], className='pl-0'), width=9),
    #             ])
    #         ),width=10),
    #         dbc.Col(width=1),

    #     ]),
    #     dbc.Col(width=1),
    # ]),
    #     dbc.Row([    
    #     dbc.Col(width=1),
    #     dbc.Col((html.Div([
    #         html.Div(style={'height': '20px'}),  # Add a space
    
    #         html.Div(style={'height': 'form0px'}),  # Add a space
    #         dbc.Row([
    #             dbc.Col(dcc.Markdown(''' ### EMPRASA: '''), width=3),
    #             dbc.Col(dcc.Dropdown(id='country-dropdown', options=[{'label': i, 'value': i} for i in ['ETICSA', 'DTS']]), width=9),
    #         ]),
    #         html.Div(style={'height': '20px'}),  # Add a space between the dropdowns
    #         dbc.Row([
    #             dbc.Col(dcc.Markdown(''' ### ÁREA: '''), width=3),
    #             dbc.Col(dcc.Dropdown(id='city-dropdown'), width=9),
    #         ]),
    #         ])),width=10),
    #     dbc.Col(width=1)
    # ]),
    #         dbc.Row([
    #         dbc.Col(width=1),
    #         dbc.Col((
    #             dbc.Row([
    #                             dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Markdown(''' ### CENTRO COSTO: '''),
    #         ]), width=3),
    #         dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Input(
    #                 placeholder='Enter a value...',
    #                 type='text',
    #                 value='',
    #                 style={'width': '100%'}
    #             ),
    #         ], className='pl-0'), width=9),
    #             ])
    #         ),width=10),
    #         dbc.Col(width=1),

    #     ]),
    #             dbc.Row([
    #         dbc.Col(width=1),
    #         dbc.Col((
    #             dbc.Row([
    #                             dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Markdown(''' ### NOMBRE SOLICITANTE: '''),
    #         ]), width=3),
    #         dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Input(
    #                 placeholder='Enter a value...',
    #                 type='text',
    #                 value='',
    #                 style={'width': '100%'}
    #             ),
    #         ], className='pl-0'), width=9),
    #             ])
    #         ),width=10),
    #         dbc.Col(width=1),

    #     ]),
    #      dbc.Row([
    #         dbc.Col(width=1),
    #         dbc.Col((
    #             dbc.Row([
    #                             dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Markdown(''' ### NOMBRE DE QUIÉN AUTORIZA: '''),
    #         ]), width=3),
    #         dbc.Col(html.Div([
    #             html.Br(),
    #             dcc.Input(
    #                 placeholder='Enter a value...',
    #                 type='text',
    #                 value='',
    #                 style={'width': '100%'}
    #             ),
    #         ], className='pl-0'), width=9),
    #             ])
    #         ),width=10),
    #         dbc.Col(width=1),

    #     ]),
    

    ]