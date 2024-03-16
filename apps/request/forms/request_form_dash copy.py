import dash_bootstrap_components as dbc
import dash
from dash import Dash, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
import dash_daq as daq
from datetime import date

theme = dbc.themes.BOOTSTRAP

app = DjangoDash('Request_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP], meta_tags = None)



def serve_layout():  
    return dbc.Container([
        dbc.Row([
            dbc.Col(width=2),
            dbc.Col(
                        html.Div([
            dcc.Markdown(''' # Dropdown Single Value'''),
            dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
            html.Br(),
            dcc.Markdown(''' # Dropdown Multiple Value'''),
            dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal', multi=True),
            html.Br(),
            dcc.Markdown(''' # Slider Number'''),
            dcc.Slider(-5, 10, 1, value=-3),
            html.Br(),
            dcc.Markdown(''' # Slider Label'''),
            dcc.Slider(0, 9, marks={i: f'Label{i}' for i in range(10)}, value=5),
            html.Br(),
            dcc.Markdown(''' # RangeSlider Number'''),
            dcc.RangeSlider(-5, 10, 1, count=1, value=[-3, 7]),
            html.Br(),
            dcc.Markdown(''' # RangeSlider Label'''),
            dcc.RangeSlider(-5, 6,
                marks={i: f'Label{i}' for i in range(-5, 7)},
                value=[-3, 4]
            ),
            html.Br(),
            dcc.Markdown(''' # Input Value'''),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ),
            html.Br(),
            html.Br(),
            dcc.Markdown(''' # Text Area'''),
            dcc.Textarea(
                placeholder='Enter a value...',
                value='This is a TextArea component',
                style={'width': '100%'}
            ),
            html.Br(),
            html.Br(),
            dcc.Markdown(''' # Checklist column'''),
            dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                        ['Montréal', 'San Francisco']),
            html.Br(),
            dcc.Markdown(''' # Checklist Row'''),
            dcc.Checklist(
                ['New York City', 'Montréal', 'San Francisco'],
                ['Montréal', 'San Francisco'],
                inline=True
            ),
            html.Br(),
            dcc.Markdown(''' # RadioItems Column'''),
            dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
            html.Br(),
            dcc.Markdown(''' # RadioItems Row'''),
            dcc.RadioItems(
                ['New York City', 'Montréal', 'San Francisco'],
                'Montréal',
                inline=True
            ),
            html.Br(),
            dcc.Markdown(''' # Input & Submit '''),
            html.Div(dcc.Input(id='input-box', type='text')),
            html.Button('Submit', id='button-example-1'),
            html.Div(id='output-container-button',
                    children='Enter a value and press submit'),
            html.Br(),
            dcc.Markdown(''' # DatePicker '''),
            dcc.DatePickerSingle(
                id='date-picker-single',
                date=date(1997, 5, 10)
            ),
            html.Br(),
            html.Br(),
            dcc.Markdown(''' # DatePicker wiht Label '''),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=date(1997, 5, 3),
                end_date_placeholder_text='Select a date!'
            ),
            html.Br(),
            dcc.Markdown(''' # DatePicker wiht Label '''),
            html.Button("Download Text", id="btn_txt"), 
            dcc.Download(id="download-text-index"),
            html.Br(),
            dcc.Markdown(''' # Drag & Drop CSV '''),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Br(),
            dcc.Markdown(''' # Drag & Drop Image/PDF '''),
            html.Div(id='output-data-upload'),
            dcc.Upload(
                id='upload-image',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-image-upload'),
        ]),width=8),
            dbc.Col(width=2),
        ])

    ],
    fluid=True,
)

app.layout = serve_layout


@callback(
    Output('output-container-button', 'children'),
    Input('button-example-1', 'n_clicks'),
    State('input-box', 'value'))
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )

@callback(Output("download-text-index", "data"), 
          Input("btn_txt", "n_clicks"),
          prevent_initial_call=True
        )
def func(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return dict(content="Hello world!", filename="hello.txt")

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children