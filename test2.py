import matplotlib.pyplot as plt
import requests


response = requests.get('http://localhost:8001/fourier')

# Obtenemos el JSON de la respuesta
fourier_data = response.json()

# Obtenemos los datos de frecuencias y amplitudes del JSON
xf = fourier_data['frequencies']
yf = fourier_data['amplitudes']