# Análisis de artículos publicados en la revista Elementos de la BUAP

Proyecto Final de Fundamentos de Ciencia de Datos



## WebScrapping
La herramienta se encuentra desarrollada en Python y en algunos casos se complementa con ParseHub para la extracción de la información
### Funcionamiento
<ol>
  <li>Se establece una conexión con una base de datos MySQL utilizando la librería mysqlconnector de Python.</li>
  <li>La entrada de cada una de las funciones es un rango de direcciones a analizar:
      <ul>
        <li>Se descarga el código html de la página</li>
        <li>Se utiliza la libreria BeautifulSoup de Python para seleccionar la información de interés</li>
        <li>Se termina la limpieza de los datos utilizando la librería regular expressions de Python</li>
        <li>Se realiza la carga de los datos encontrados en la base de datos MySQL con la que se estableció la conexión</li>
      </ul>
    </li>
</ol>
