<div class="markdown prose w-full break-words dark:prose-invert light">

<h1>Aplicación Flask para análisis de demanda energética</h1>

<p>Esta es una aplicación Flask que recupera datos de demanda energética de una API, realiza una Transformada Rápida de Fourier en los datos y envía los resultados al usuario en forma de gráfico. El usuario también puede descargar los datos en bruto como un archivo JSON.</p>

<h2>Rutas</h2>

<p>La aplicación tiene cuatro rutas:</p>
<ul><li><code>/</code>: La página de inicio, que contiene un formulario que permite al usuario especificar el rango de fechas para el cual desea recuperar datos.</li>
<li><code>/fft</code>: La ruta que recupera los datos de la API y los guarda en un archivo.</li>
<li><code>/download_json</code>: La ruta que permite al usuario descargar los datos en bruto como un archivo JSON.</li>
<li><code>/grafico</code>: La ruta que genera el gráfico de la FFT.</li>
<li><code>/results</code>: La página con los botones para poder gestionar los anteriores puntos</li>
</ul>

<h2>Paquetes utilizados</h2>

<p>La aplicación utiliza los siguientes paquetes:</p>
<ul><li>requests</li>
<li>json</li>
<li>pandas</li>
<li>numpy</li>
<li>scipy</li>
<li>Flask</li>
<li>matplotlib</li>
</ul>
</div>
