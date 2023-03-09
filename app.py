import requests
import json
import pandas as pd
import numpy as np
from scipy.fft import fft
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file, session
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
from graphs import graphs
import socket

app = Flask(__name__) 
app.secret_key = '94318075c5'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')

server_url = os.environ.get('SERVER_URL')

@app.route('/fft', methods=['GET', 'POST'])
def fft_endpoint():
    token = 'f9cc0ba317d94318075c597df818c413def16b7046acb73099f59b728fa2ab7e'
    variable_id = '1293'
    url = 'https://api.esios.ree.es/indicators/1293'
    # Define los encabezados de la solicitud
    headers = {
            "Accept": "Accept: application/json; application/vnd.esios-api-v2+json",
            "Content-Type": "application/json",
            "x-api-key": token
        }

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
    else:
        start_date = '2018-09-02T00:00:00'
        end_date = '2018-10-06T23:59:59'
        
    response = requests.get(url, headers=headers, params={"start_date": start_date, "end_date": end_date})

    # Si la respuesta HTTP fue exitosa (código 200), almacena la variable data en una variable de sesión
    if response.status_code == 200:
        data = response.json()
        session['data'] = data
        # Guardar la data en un archivo en el servidor
        filename = 'data.json'
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # app.config['UPLOAD_FOLDER'] debe ser la ruta a la carpeta en el servidor donde deseas guardar el archivo
        with open(path, 'w') as f:
            f.write(json.dumps(data))
        # Devolver la respuesta como JSON
        jsonify(data)
        return render_template("results.html")
    
    else:
        # En caso contrario, devuelve un mensaje de error con el código de estado de la respuesta
        return f"Error: {response.status_code}"


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

@app.route('/demanda_json')
def demanda_json():        
        # Cargamos los datos del archivo data.json
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'data.json')
        with open(filename, 'r') as f:
           data = json.load(f)
        values = data['indicator']['values']
        data_list = [] 
        for value in values:
                data_dict = {}
                data_dict['datetime'] = value['datetime']
                data_dict['value'] = value['value']
                data_list.append(data_dict)

        # Creamos el DataFrame a partir de la lista de diccionarios
        df = pd.DataFrame(data_list)

            # Convertimos la columna 'datetime' a un objeto datetime y la establecemos como índice del DataFrame
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')

                # Calculamos el valor promedio de la demanda eléctrica para cada hora en el período
        hourly_data = df.groupby(pd.Grouper(freq='H')).mean()
        hourly_data = hourly_data.dropna()
        # Realizar el cálculo de la transformada de Fourier de la demanda eléctrica
        n = len(hourly_data)
        yf = np.fft.fft(hourly_data['value'].values)
        xf = np.linspace(0.0, 1.0/(2.0*60*60), n//2)
        
        # Preparamos los datos para ser devueltos en formato JSON
        data = []
        for i in range(len(hourly_data)):
            item = {
                'datetime': str(hourly_data.index[i]),
                'value': hourly_data['value'][i]
            }
            data.append(item)
        
        # Agregamos los datos de la transformada de Fourier al diccionario
        demanda_json = {'data': data, 'frecuencias': xf.tolist(), 'transformada': (2.0/int(n) * np.abs(yf[0:int(n)//2])).tolist()}
        
        # Escribimos el diccionario en un archivo JSON
        with open('demanda_transformada.json', 'w') as f:
            json.dump(demanda_json, f)
    
    # Enviamos el archivo JSON como respuesta HTTP
        return send_file('demanda_transformada.json', as_attachment=True)
        

@app.route('/')
def index():
        return render_template("index.html")


def get_server_url():
    # Obtener la URL del servidor desde la variable de entorno 'SERVER_URL'
    server_url = os.getenv('SERVER_URL')

    # Si no se ha establecido una variable de entorno, usar una URL predeterminada
    if not server_url:
        server_url = 'http://localhost:5000'

    return server_url



@app.route('/grafico', methods=['GET', 'POST'])
def grafico():
    server_url = get_server_url()
    url = f'{server_url}/demanda_json'
    html = graphs(url)
    return html

@app.route('/results')
def results():
        return render_template("results.html")


@app.route('/download_json')
def download_json():
    # Ruta al archivo data.json
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'data.json')
    # Enviar el archivo como respuesta HTTP
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run()