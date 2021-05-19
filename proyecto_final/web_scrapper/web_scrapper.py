# -*- coding: utf-8 -*-

import urllib.request as url
from bs4 import BeautifulSoup
import re
from proyecto_final.mysqlconnector.connection import connect

def titulos(x):
    url_base_ = "https://elementos.buap.mx/num_single.php?num="
    query = ("INSERT INTO numeros VALUES (%(Numero_)s, %(Num_Address_)s, %(Titulo_)s);")
    cnx,cursor = mysql_connection()
    for i in x:
        nombre_ = ""
        try:
            html_ = url.urlopen(url_base_+str(i))
            soup = BeautifulSoup(html_,'html.parser')
            print("Descarga exitosa de: "+url_base_+str(i))
            for tag in soup.find_all(True):
                if tag.name == 'button' and tag.has_attr('class'):
                    if 'btn-danger' in tag['class']:
                        nombre_ = re.sub(r'[\n\r]','',tag.string).strip()

            data_ = {
                'Numero_' : i,
                'Num_Address_' : url_base_+str(i),
                'Titulo_': nombre_
            }
            
            cursor.execute(query,data_)
            cnx.commit()
            print("Query completo de Elementos Número "+str(i))

        except mysql.connector.Error as err:
            if err != -1:
                print(err)
                cursor.close()
                cnx.close()
    
    cursor.close()
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


def get_temas ():
    url_head = "https://search.scielo.org/?q=lenguaje&lang=es&count=15&from=0&output=site&sort=&format=summary&fb=&page=1&q="
    url_tail = "&lang=es&page=1"
    clasif = ["Ciencias de la Salud", "Humanidades", "Ciencias Sociales Aplicadas", "Ciencias Agrícolas", "Ciencias Biológicas","Ciencias Exactas y de la Tierra","Ingenierias","Multidisciplinaria","Lingüistica, Letras y Artes"]
    i = 0
    cnx,cursor = connect( user = "root", password = "123456", host = "127.0.0.1", database = "modelo_multimencional_elementos" )
    cursor.callproc("getMaxPalabraXArticulo")

    cnx2,cursor2 = connect( user = "root", password = "123456", host = "127.0.0.1", database = "cd_elementos" )
    query = ("INSERT INTO temaspalabras VALUES (%(palabra_)s, %(IDArticulo_)s, %(Tema_)s, %(CuentaArticulos_)s);")

    for result in cursor.stored_results():
        cursor_buff = result.fetchall()
        for (Palabra, Rep, IdRev, IdAutor, IdArt ) in cursor_buff:
            try:
                html_ = url.urlopen(url_head+Palabra+url_tail)
                soup = BeautifulSoup(html_,'html.parser')
                for tag in soup.find_all("li"):
                    if tag.has_attr("data-item"):
                        if tag["data-item"] in clasif:
                            data_ = {
                               "palabra_"       :   Palabra,
                               "IDArticulo_"     :   IdArt,
                               "Tema_"          :   tag["data-item"],
                               "CuentaArticulos_":  tag["data-count"]
                            }
                            cursor2.execute(query,data_)
                            cnx2.commit()
                print(IdArt)

            except:pass
            