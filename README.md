# Análisis de artículos publicados en la revista Elementos de la BUAP

Proyecto Final de la materia de Fundamentos de Ciencia de Datos.
El objetivo es construir un modelo multidimensional que facilite el análisis de la información disponible de la publicación. Se analizan números (revistas/publicaciones), autores y artículos que se encuentran en forma digital en la página:https://elementos.buap.mx/

## Primera Parte: Descarga de bases de datos - WebScrapping
La herramienta se encuentra desarrollada en Python y en algunos casos se complementa con ParseHub para la extracción de contenidos.

### Librerias
<ul>
  <li>MySQL Connector</li>
  <li>BeautifulSoup</li>
  <li>Regular Expressions</li>
</ul>

### Funcionamiento
<ol>
  <li>Se establece una conexión con una base de datos MySQL utilizando la librería mysqlconnector de Python.</li>
  <li>La entrada de cada una de las funciones es un rango de direcciones a analizar:
      <ul>
        <li>Se descarga el código html de la página</li>
        <li>Seleccionar la información de interés</li>
        <li>Limpieza adicional de los datos</li>
        <li>Se realiza la carga de los datos encontrados en la base de datos MySQL con la que se estableció la conexión</li>
      </ul>
    </li>
  <li>Cierre de conexión con base de datos</li>
</ol>
