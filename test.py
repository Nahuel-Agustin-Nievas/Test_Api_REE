import matplotlib.pyplot as plt
import requests

response = requests.get('http://localhost:8001/fourier')

# Obtenemos el JSON de la respuesta
fourier_data = response.json()

# Obtenemos los datos de frecuencias y amplitudes del JSON
xf = fourier_data['frequencies']
yf = fourier_data['amplitudes']

# Creamos el gráfico de la transformada de Fourier
fig, ax = plt.subplots()
ax.plot(xf, yf)
ax.set_xlabel('Frecuencia (Hz)')
ax.set_ylabel('Amplitud')
ax.set_title('Transformada de Fourier')
plt.show() 