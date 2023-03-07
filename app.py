import requests
import pandas as pd
import numpy as np
from scipy.fft import fft
from flask import Flask, jsonify
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import os

app = Flask(__name__)

# Token de acceso a la API de REE
token = 'f9cc0ba317d94318075c597df818c413def16b7046acb73099f59b728fa2ab7e'
# URL del indicador de Demanda Real
url = 'https://api.esios.ree.es/indicators/1293'

# Define los encabezados de la solicitud
headers = {
    "Accept": "Accept: application/json; application/vnd.esios-api-v2+json",
    "Content-Type": "application/json",
    "x-api-key": token
}

# Realiza la solicitud GET y obtiene la respuesta
response = requests.get(url, headers=headers, params={"start_date": "2018-09-02T00:00:00", "end_date": "2018-10-06T23:59:59"})

# Si la respuesta HTTP fue exitosa (código 200), obtiene el contenido de la respuesta
if response.status_code == 200:
    data = response.json()
    # Hacer algo con los datos obtenidos, como imprimirlos en la consola
    # print(data)
    # Extraemos los datos relevantes del JSON y los guardamos en una lista de diccionarios
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

    # Realizamos la transformada de Fourier
    n = len(hourly_data)
    yf = fft(hourly_data['value'].to_numpy())
    xf = np.linspace(0.0, 1.0/(2.0*60*60), n//2)

   # Definimos el endpoint que devuelve la transformada de Fourier en formato JSON
    @app.route('/fourier', methods=['GET'])
    def get_fourier():
        # Creamos un diccionario con los datos de la transformada de Fourier
        fourier_data = {
            'frequencies': xf.tolist(),
            'amplitudes': np.abs(yf[0:n//2]).tolist()
        }
        # Devolvemos los datos en formato JSON
        return jsonify(fourier_data)    


@app.route('/demanda_json')
def demanda_json():
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
    
    # Devolver los datos en formato JSON
    return jsonify(demanda_json)


@app.route('/abrir_grafico')
def abrir_grafico():
    os.system('python graphs1.py')
    return 'Archivo abierto'

if __name__ == '__main__':
    app.run(debug=True, port=8001)