import matplotlib
matplotlib.use('Agg')
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import DayLocator, DateFormatter
from flask import send_file
import os
from io import BytesIO
import base64

def graphs(url):
    # Realizar la petición GET a la ruta /demanda_json y obtener los datos en formato JSON
    response = requests.get(url)
    data = json.loads(response.text)

    # Obtener los datos de la demanda eléctrica en función del tiempo
    datetime_values = [datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S%z') for item in data['data']]
    demand_values = [item['value'] for item in data['data']]

    # Crear el gráfico de la demanda eléctrica en función del tiempo  
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    axs[0].plot(datetime_values, demand_values)
    axs[0].set_xlabel('Tiempo') 
    axs[0].set_ylabel('Demanda eléctrica') 
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y')) 
    axs[0].xaxis.set_major_locator(DayLocator())
    axs[0].tick_params(axis='x', rotation=45)
    # Obtener los datos de la transformada de Fourier  
    freq_values = data['frecuencias']  
    transform_values = data['transformada']  
 
    # Crear el gráfico de la transformada de Fourier  
    axs[1].plot(freq_values, transform_values)   
    axs[1].set_xlabel('Frecuencia(HZ)')    
    axs[1].set_ylabel('Transformada de Fourier') 

    fig.subplots_adjust(hspace=0.5)
 
     # Crear el gráfico de la transformada de Fourier  
    axs[1].plot(freq_values, transform_values)   
    axs[1].set_xlabel('Frecuencia(HZ)')    
    axs[1].set_ylabel('Transformada de Fourier') 
 
     # Guardar el gráfico en un archivo PNG y codificarlo en base64
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_string = base64.b64encode(buffer.read()).decode('utf-8')

    # Cerrar la figura para liberar memoria
    plt.close(fig)

    # Retornar el código HTML para mostrar la imagen y permitir su descarga
    html = '''
    <html>
        <body>
            <h1>Gráfico</h1>
            <img src="data:image/png;base64,{}" alt="grafico_personalizado.png">
            <br>
            <a href="/grafico.png" download="grafico_personalizado.png">Descargar</a>
            <button onclick="history.back()">Volver atrás</button>
        </body>
    </html>
    '''.format(image_string)
    return html
    

    