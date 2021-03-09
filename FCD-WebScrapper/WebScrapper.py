#Librerias

import urllib.request as url                #Realizar la conexión con la página web y descargar el html
from bs4 import BeautifulSoup               #Realizar la navegación, selección y limpieza de datos del html
import mysql.connector                      #Conexión con el servidor MySQL
from mysql.connector import errorcode       #Error Handling de la conexión con servidor MySQL
import re                                   #Limpieza adicional de los datos obtenidos con BeautifulSoup


#Gestión de la conexión al SMBD
def mysql_connection():
    try:
        cnx = mysql.connector.connect(user='user',              #Cambiar usuario de acuerdo a configuración local
                                  password='password',            #Cambiar contraseña de acuerdo a configuración local
                                  host='127.0.0.1',
                                  database='cd_elementos')
        print("Conexión exitosa a la base de datos")
        print(cnx)
        cursor = cnx.cursor()                                   #Creación del cursor (herramienta para realizar queries en SQL)
        return cnx, cursor
    except mysql.connector.Error as err:                        #Error Handling de la conexión al SMBD
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuario o contraseña incorrectos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)

#Extracción de títulos de Números de la revista Elementos
def titulos(x):                                                                             #La función toma como entrada una lista de enteros, 
                                                                                            #que representan las páginas que se visitarán

    url_base_ = "https://elementos.buap.mx/num_single.php?num="                             #URL base de la página a análizar

    query = ("INSERT INTO numeros VALUES (%(Numero_)s, %(Num_Address_)s, %(Titulo_)s);")    #Definición del Query para la subida de datos al SMBD

    cnx,cursor = mysql_connection()                                                         #Conexión al SMBD

    for i in x:                                                                             #Este ciclo, visitará cada una de las direcciones para extraer
                                                                                            #seleccionar y limpiar la información

        nombre_ = ""                                                                        #Cada inicio de ciclo se vacía la variable para evitar duplicar información
        try:
            html_ = url.urlopen(url_base_+str(i))                                           #Se intenta abrir la página web indicada
            soup = BeautifulSoup(html_,'html.parser')                                       #Se utiliza beautifulSoup para hacer el parsing del html descargado
            print("Descarga exitosa de: "+url_base_+str(i))

            for tag in soup.find_all(True):                                                 #Se analizan todos los elementos de la página descargada
                if tag.name == 'button' and tag.has_attr('class'):                          #Si alguno de ellos es del tipo "button" y tiene su atributo class contiene
                                                                                            #el elemento 'btn-danger', el texto contenido se trata del nombre de la
                                                                                            #publicación
                    if 'btn-danger' in tag['class']:
                        nombre_ = re.sub(r'[\n\r]','',tag.string).strip()

            data_ = {                                                                       #Se almacenan los datos descargados en una lista de acuerdo al formato del query
                'Numero_' : i,
                'Num_Address_' : url_base_+str(i),
                'Titulo_': nombre_
            }
            
            cursor.execute(query,data_)                                                     #Se realiza el Query
            cnx.commit()                                                                    #Y se confirma
            print("Query completo de Elementos Número "+str(i))

        except mysql.connector.Error as err:                                                #Gestión de errores
            if err != -1:
                print(err)
                cursor.close()
                cnx.close()
    
    cursor.close()                                                                          #Se cierra la conexión con nuestro SMBD
    cnx.close()

def articulos(x):
    url_base_ = "https://elementos.buap.mx/num_single.php?num="
    query = ("INSERT INTO InfoArticulos VALUES (%(Numero_)s, %(Titulo_art)s, %(Autor_)s, %(URL_)s);")
    cnx,cursor = mysql_connection()
    for i in x:
        titulo_art = []
        autor_ = []
        url_=[]

        try:
            html_ = url.urlopen(url_base_+str(i))
            soup = BeautifulSoup(html_,'html.parser')
            print("Descarga de html completa "+url_base_+str(i))

            for tag in soup.find_all(True):
                if tag.name == 'h3' and tag['style'] == 'color:rgb(20, 111, 156)':
                    titulo_art.append(re.sub(r'[\n\r]','',tag.string).strip())
                if tag.name == 'a' and tag.has_attr('style'):
                    autor_.append(re.sub(r'[\n\r,]','',tag.string).strip())
                if tag.name == 'a' and tag.has_attr('class'):
                    if 'see-article' in tag['class']:
                        url_.append(tag['href'])

            for j in range(0,len(titulo_art)):
                data_ = {
                    'Numero_' : i,
                    'Titulo_art' : titulo_art[j],
                    'Autor_': autor_[j],
                    'URL_':url_[j]
                }
                cursor.execute(query,data_)
                cnx.commit()
                print("Carga de articulo "+str(i)+"-"+str(j+1)+" Completa")

        except mysql.connector.Error as err:
            if err != -1:
                print(err)
                cursor.close()
                cnx.close()
    
    cursor.close()
    cnx.close()

def contenido_articulo(x):
    url_base_ = "https://elementos.buap.mx/post.php?id="
    query_ = ("INSERT INTO articulos VALUES (%(Art_Num_)s, %(Address_)s, %(Articulo_)s);")
    cnx,cursor = mysql_connection()
    for i in x:
        article_ = ""
        try:
            html_ = url.urlopen(url_base_+str(i))
            soup = BeautifulSoup(html_,'html.parser')
            print("html download succesfull from "+url_base_+str(i))

            for tag in soup.find_all(True):
                if tag.name == 'div' and tag.has_attr('class'):
                    if 'contenido' in tag['class']:
                        article_ = tag.get_text(separator="\n").strip().replace("\xa0","")
                            
            data_ = {
                'Art_Num_' : i,
                'Address_' : url_base_+str(i),
                'Articulo_': article_
                }
                
            cursor.execute(query_,data_)
            cnx.commit()
            print("Carga de articulo "+str(i)+" Completa")

        except mysql.connector.Error as err:
            if err != -1:
                print(err)
                cursor.close()
                cnx.close()
    cursor.close()
    cnx.close()

def autores(x):
    url_base_ = "https://elementos.buap.mx/authors_single.php?id="
    for i in x:
        try:
            opener = url.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            html_ = opener.open(url_base_+str(i))
            soup = BeautifulSoup(html_,'html.parser')
            empty_author = False
            for tag in soup.find_all(True):
                if tag.name == 'h2' and not tag.has_attr('class'):
                    if 'Por el momento no hay artículos individuales.' in tag.get_text():
                        empty_author = True
            if not empty_author:
                print(i)
        except: pass
