import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
from apps.request.models import CotizacionRealizada, CotizacionRealizada_Productos, CotizacionRealizada_Archivos, Estado_Solicitudes
import dash_daq as daq
from datetime import date
from apps.request.forms_content.cotizacion_realizada import form_cotizacion_realizada, save_button2, message_alert
from apps.request.forms_content.solicitud_cotizacion import form_solicitud_cotizacion, save_button2, message_alert
from django.contrib.auth.decorators import login_required

import base64
import datetime    
import io
import os

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

theme = dbc.themes.BOOTSTRAP

app = DjangoDash('Request_DashApp', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP])

file_data = []

area_options = {
    'ETICSA': ['SERVICIOS', 'INTEGRACIÓN'],
    'DTS': ['SERVICIOS', 'PROYECTOS']
}

#df_cotizacion_realizada = pd.DataFrame(columns=['User_Id', 'User_Name','Formulario', 'Nombre Proveedor', 'Rut_Proveedor', 'Empresa', 'Area', 'Centro Costo', 'Nombre Solicitante', 'Nombre de Quién Autoriza', 'Nombre Producto', 'Cantidad', 'Descripción Producto'])
df_cotizacion_realizada = pd.DataFrame(columns=['User_Id', 'User_Name','Formulario', 'Nombre Proveedor', 'Rut_Proveedor', 'Empresa', 'Area', 'Centro Costo', 'Nombre Solicitante', 'Nombre de Quién Autoriza'])
df_cotizacion_realizada_productos = pd.DataFrame(columns=['Nombre Producto', 'Cantidad', 'Descripción Producto'])

df_solicitud_cotizacion = pd.DataFrame(columns=['User_Id', 'User_Name','Formulario', 'Nombre Proveedor', 'Rut_Proveedor', 'Empresa', 'Area', 'Centro Costo', 'Nombre Solicitante', 'Nombre de Quién Autoriza'])
df_solicitud_cotizacion_productos = pd.DataFrame(columns=['Nombre Producto', 'Cantidad', 'Descripción Producto'])




def serve_layout():  
    return dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(style={'height': '20px'}), width=12)
    ]),

    dbc.Row([    
        dbc.Col(width=2),
        dbc.Col((html.Div([
            html.Div(style={'height': '20px'}),  # Add a space
            dcc.Markdown(''' #### EMPRESA: '''),
            html.Div(style={'height': '40px'}),  # Add a space
            dcc.Dropdown(id='empresa-dropdown', options=[{'label': i, 'value': i} for i in ['ETICSA', 'DTS']]),
            
            ])),width=8),
        dbc.Col(width=2)
    ]), 
    dbc.Row([    
        dbc.Col(width=2),
        dbc.Col((html.Div([
            html.Div(style={'height': '20px'}),  # Add a space
            dcc.Markdown(''' #### SELECCIONE \'SOLICITUD FORMULARIO\' '''),
            html.Div(style={'height': '40px'}),  # Add a space
            dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i} for i in ['Cotización Realizada', 'Solicitud de Cotización']],),
            html.Br(),
            dbc.Button('Submit', id='submit-button', style={'display': 'block'}, n_clicks=0),
            ])),width=8),
        dbc.Col(width=2)
    ]), 
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col(html.Div(id='output-container', style={'display': 'block'}), width=10),  # Agregamos el estilo inicial aquí
            dbc.Col(width=1),
        ]),

        dcc.ConfirmDialog(
    id='confirm',
    message='',
),
        dbc.Row([
        dbc.Col(width=1),
        dbc.Col(html.Div(id='output-container2'), width=10),
        
        dbc.Col(width=1),
    ]),    

    html.Div(id='user_id', style={'display': 'none'}),
    html.Div(id='username', style={'display': 'none'}),
    html.Div(id='email', style={'display' : 'none'})    
    ],
    fluid=True,
    style={'padding-bottom':'200px'}
)

app.layout = serve_layout


@app.callback(
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('dropdown', 'value'),
    State('empresa-dropdown', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value, selected_company):
    print('**')
    print(value)
    if n_clicks > 0:
        selected_company = [{'label': i, 'value': i} for i in area_options[selected_company]]
        if value == 'Cotización Realizada':
            return form_cotizacion_realizada(selected_company)
        elif value == 'Solicitud de Cotización':
            return form_solicitud_cotizacion(selected_company)
    else:
        return []


# @app.callback(
#     Output('area-dropdown', 'options'),
#     Input('empresa-dropdown', 'value'),
#     prevent_initial_call=True
# )
# def update_area_dropdown(selected_company):
#     return [{'label': i, 'value': i} for i in area_options[selected_company]]

@app.callback(
    [Output('table_producto', 'data'),
     Output('input_nombre_producto', 'value'),
     Output('input_cantidad', 'value'),
     Output('input_descripcion_producto', 'value')],
    Input('editing-rows-button', 'n_clicks'),
    State('table_producto', 'data'),
    State('table_producto', 'columns'),
    State('input_nombre_producto', 'value'),
    State('input_cantidad', 'value'),
    State('input_descripcion_producto', 'value')
)
def add_row(n_clicks, rows, columns, nombre_producto, cantidad, descripcion_producto):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
        # Agregamos los valores ingresados a la última fila
        rows[-1]['Nombre Producto'] = nombre_producto
        rows[-1]['Cantidad'] = cantidad
        rows[-1]['Descripción Producto'] = descripcion_producto
        # Limpiamos los campos de entrada
        nombre_producto = ''
        cantidad = ''
        descripcion_producto = ''
    return rows, nombre_producto, cantidad, descripcion_producto

@app.callback(
    [Output("confirm", "displayed"), Output("confirm", "message")],
    [Input("save-button", "n_clicks")]
)
def open_confirm_dialog(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return True, "¿Está seguro de guardar la información?"
    return False, ""


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    file_type = os.path.splitext(filename)[1][1:]
    return {
        'File Number': len(file_data) + 1,
        'File Name': filename,
        'File Type': file_type,
        'Content': decoded
    }

@app.callback(Output('store-data-upload', 'data'),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified'))
def update_upload(list_of_contents, list_of_names, list_of_dates):
    global file_data
    if list_of_contents is not None:
        data = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        file_data.extend(data)
        return [{'File Number': f['File Number'], 'File Name': f['File Name'], 'File Type': f['File Type']} for f in file_data]

@app.callback(Output('data-table', 'data'),
            Input('store-data-upload', 'data'))
def update_table(data):
    if data is not None:
        df = pd.DataFrame(data)
        return df.to_dict('records')


@app.callback(
    [Output('output-container2', 'children'),
    Output('output-container', 'style'),
    Output('submit-button','style')],  # nuevo Output
    [Input('confirm', "submit_n_clicks"),
     Input('table_producto', 'data'),
     Input('data-table', 'data')], 
    [State('dropdown','value'),
     State('input_nombre_proveedor', 'value'),
     State('input_rut_proveedor', 'value'),
     State('empresa-dropdown', 'value'),
     State('area-dropdown', 'value'),
     State('input_centro_costo', 'value'),
     State('input_nombre_solicitante', 'value'),
     State('input_nombre_autoriza', 'value'),
     State('user_id', 'children'),
     State('username', 'children'),
     State('confirm', 'displayed')],
    prevent_initial_call=True
)
def update_output2(submit_n_clicks, table_producto, table_data, value, nombre_proveedor, rut_proveedor, empresa_value, area_value, centro_costo, nombre_solicitante, nombre_autoriza, user_id, username, is_confirm_open,request):
    global file_data
    if value == 'Cotización Realizada':
        if submit_n_clicks is not None and submit_n_clicks > 0:
            if not area_value:
                return message_alert('Información incompleta - Agregar Valor Área')
            elif not centro_costo:
                return message_alert('Información incompleta - Agregar Valor Centro de Costo')
            elif not nombre_solicitante:
                return message_alert('Información incompleta - Agregar Valor Nombre Solicitante')
            elif not nombre_autoriza:
                return message_alert('Información incompleta - Agregar Valor Nombre de Quién Autoriza')
            # elif not table_producto or len(table_producto) == 0:
            #     return message_alert('Información incompleta - Agregar valores en Tabla Productos')
            elif not table_data or len(table_data) == 0:
                return message_alert('Información incompleta - Agregar Documentos')
            elif nombre_proveedor and rut_proveedor and empresa_value and area_value and centro_costo and nombre_solicitante and nombre_autoriza:
                user = request.user
                user_id = user.id
                username = user.username
                user_email = user.email
                df_cotizacion_realizada = pd.DataFrame({
                    "User_Id": [user_id],
                    "User_Name": [username],
                    "Formulario": ["Cotización Realizada"],
                    "Nombre Proveedor": [nombre_proveedor],
                    "Rut_Proveedor": [rut_proveedor],
                    "Empresa": [empresa_value],
                    "Area": [area_value],
                    "Centro Costo": [centro_costo],
                    "Nombre Solicitante": [nombre_solicitante],
                    "Nombre de Quién Autoriza": [nombre_autoriza],
                })
                df_cotizacion_realizada_productos = pd.DataFrame(table_producto)
                cotizacion_realizada = CotizacionRealizada.objects.create(
                    User_Id=user_id,
                    User_Name=username,
                    Formulario="Cotización Realizada",
                    Nombre_Proveedor=nombre_proveedor,
                    Rut_Proveedor=rut_proveedor,
                    Empresa=empresa_value,
                    Area=area_value,
                    Centro_Costo=centro_costo,
                    Nombre_Solicitante=nombre_solicitante,
                    Nombre_Autoriza=nombre_autoriza,
                )
                if table_producto is None:
                    table_producto = []
                else:
                    for producto in table_producto:
                        CotizacionRealizada_Productos.objects.create(
                            ID_OC=cotizacion_realizada,
                            Nombre_Producto=producto['Nombre Producto'],
                            Cantidad=producto['Cantidad'],
                            Descripcion_Producto=producto['Descripción Producto'],
                        )
                for archivo in table_data:
                    CotizacionRealizada_Archivos.objects.create(
                        ID_OC=cotizacion_realizada,
                        File_Number=archivo['File Number'],
                        File_Name=archivo['File Name'],
                        File_Type=archivo['File Type'],
                    )
                
                Estado_Solicitudes.objects.create(
                    ID_OC=cotizacion_realizada,
                )
                    
            return save_button2(dbc.Alert( [ html.I(className="bi bi-check-circle-fill me-2"), "Solicitud cargada exitosamente", ], color="success", className="d-flex align-items-center", ), df_cotizacion_realizada.to_dict('records'), df_cotizacion_realizada_productos.to_dict('records'), table_data, file_data, user_email), {'display': 'none'}, {'display': 'none'}  # nuevo retorno
        elif submit_n_clicks == 0:
            return '', {'display': 'block'}, {'display': 'block'}
        else:
            return '', {'display': 'block'}, {'display': 'block'}
    
    elif value == 'Solicitud de Cotización':
        if submit_n_clicks is not None and submit_n_clicks > 0:
            if not area_value:
                return message_alert('Información incompleta - Agregar Valor Área')
            elif not centro_costo:
                return message_alert('Información incompleta - Agregar Valor Centro de Costo')
            elif not nombre_solicitante:
                return message_alert('Información incompleta - Agregar Valor Nombre Solicitante')
            elif not nombre_autoriza:
                return message_alert('Información incompleta - Agregar Valor Nombre de Quién Autoriza')
            elif not table_producto or len(table_producto) == 0:
                return message_alert('Información incompleta - Agregar valores en Tabla Productos')
            # elif not table_data or len(table_data) == 0:
            #     return message_alert('Información incompleta - Agregar Documentos')
            elif nombre_proveedor and rut_proveedor and empresa_value and area_value and centro_costo and nombre_solicitante and nombre_autoriza:
                user = request.user
                user_id = user.id
                username = user.username
                user_email = user.email
                df_solicitud_cotizacion = pd.DataFrame({
                    "User_Id": [user_id],
                    "User_Name": [username],
                    "Formulario": ["Solicitud de Cotización"],
                    "Nombre Proveedor": [nombre_proveedor],
                    "Rut_Proveedor": [rut_proveedor],
                    "Empresa": [empresa_value],
                    "Area": [area_value],
                    "Centro Costo": [centro_costo],
                    "Nombre Solicitante": [nombre_solicitante],
                    "Nombre de Quién Autoriza": [nombre_autoriza],
                })
                df_solicitud_cotizacion_productos = pd.DataFrame(table_producto)
                solicitud_cotizacion = CotizacionRealizada.objects.create(
                    User_Id=user_id,
                    User_Name=username,
                    Formulario="Solicitud de Cotización",
                    Nombre_Proveedor=nombre_proveedor,
                    Rut_Proveedor=rut_proveedor,
                    Empresa=empresa_value,
                    Area=area_value,
                    Centro_Costo=centro_costo,
                    Nombre_Solicitante=nombre_solicitante,
                    Nombre_Autoriza=nombre_autoriza,
                )


                for producto in table_producto:
                    CotizacionRealizada_Productos.objects.create(
                        ID_OC=solicitud_cotizacion,
                        Nombre_Producto=producto['Nombre Producto'],
                        Cantidad=producto['Cantidad'],
                        Descripcion_Producto=producto['Descripción Producto'],
                    )
                if table_data is None:
                    table_data = []
                else:
                    for archivo in table_data:
                        CotizacionRealizada_Archivos.objects.create(
                            ID_OC=solicitud_cotizacion,
                            File_Number=archivo['File Number'],
                            File_Name=archivo['File Name'],
                            File_Type=archivo['File Type'],
                        )
                Estado_Solicitudes.objects.create(
                    ID_OC=solicitud_cotizacion,
                )

            return save_button2(dbc.Alert( [ html.I(className="bi bi-check-circle-fill me-2"), "Solicitud cargada exitosamente", ], color="success", className="d-flex align-items-center", ), df_solicitud_cotizacion.to_dict('records'), df_solicitud_cotizacion_productos.to_dict('records'), table_data, file_data, user_email), {'display': 'none'}, {'display': 'none'}  # nuevo retorno
        elif submit_n_clicks == 0:
            return '', {'display': 'block'}, {'display': 'block'}

        else:
            return '', {'display': 'block'}, {'display': 'block'}








