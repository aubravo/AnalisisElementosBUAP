from bs4 import BeautifulSoup
import urllib.request as url
import mysql.connector
from mysql.connector import errorcode
import re

def titulos(x):
    url_base_ = "https://elementos.buap.mx/num_single.php?num="
    query = ("INSERT INTO numeros VALUES (%(Numero_)s, %(Num_Address_)s, %(Titulo_)s);")
    try:
        cnx = mysql.connector.connect(user='root', password='123456',
                                  host='127.0.0.1',
                                  database='cd_elementos')
        print("Connected to database:")
        print(cnx)
        cursor = cnx.cursor()
        for i in x:
            nombre_ = ""
            try:
                html_ = url.urlopen(url_base_+str(i))
                soup = BeautifulSoup(html_,'html.parser')
                print("html download succesfull from "+url_base_+str(i))

                for tag in soup.find_all(True):
                    if tag.name == 'h3' and tag['style'] == 'color:rgb(20, 111, 156)':
                        print(re.sub(r'[\n\r]','',tag.string).strip())
                    if tag.name == 'a' and tag.has_attr('style'):
                        print(re.sub(r'[\n\r,]','',tag.string).strip())
            
                data_ = {
                    'Numero_' : i,
                    'Num_Address_' : url_base_+str(i),
                    'Titulo_': nombre_
                    }

            
                print("ready for query")
                cursor.execute(query,data_)
                cnx.commit()
                print("query complete")

            except mysql.connector.Error as err:
                if err != -1:
                    print(err)
                else:
                    raise            

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
        print("something went wrong")
        cursor.close()
        cnx.close()

def articulos(x):
    url_base_ = "https://elementos.buap.mx/num_single.php?num="
    query = ("INSERT INTO InfoArticulos VALUES (%(Numero_)s, %(Titulo_art)s, %(Autor_)s, %(URL_)s);")
    try:
        cnx = mysql.connector.connect(user='root', password='123456',
                                  host='127.0.0.1',
                                  database='cd_elementos')
        print(cnx)
        cursor = cnx.cursor()
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
                else:
                    raise            

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
        cursor.close()
        cnx.close()


def contenido_articulo(x):
    url_base_ = "https://elementos.buap.mx/post.php?id="
    query_ = ("INSERT INTO articulos VALUES (%(Art_Num_)s, %(Address_)s, %(Articulo_)s);")
    try:
        cnx = mysql.connector.connect(user='root', password='123456',
                                  host='127.0.0.1',
                                  database='cd_elementos')
        print(cnx)
        cursor = cnx.cursor()
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
                else:
                    raise            

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
        cursor.close()
        cnx.close()

def autores(x):
    url_base_ = "https://elementos.buap.mx/authors_single.php?id="
    query = ("INSERT INTO InfoArticulos VALUES (%(Numero_)s, %(Titulo_art)s, %(Autor_)s, %(URL_)s);")
    try:
        cnx = mysql.connector.connect(user='root', password='123456',
                                  host='127.0.0.1',
                                  database='cd_elementos')
        print(cnx)
        cursor = cnx.cursor()
        for i in x:
            titulo_art = []
            url_=[]

            try:
                opener = url.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                html_ = opener.open(url_base_+str(i))
                soup = BeautifulSoup(html_,'html.parser')
                #print("Descarga de html completa "+url_base_+str(i))
                empty_author = False

                for tag in soup.find_all(True):
                    if tag.name == 'h2' and not tag.has_attr('class'):
                        if 'Por el momento no hay artículos individuales.' in tag.get_text():
                            empty_author = True
               
                if not empty_author:
                   print(i)
                       

                #for j in range(0,len(titulo_art)):
                #    data_ = {
                #        'Numero_' : i,
                #        'Titulo_art' : titulo_art[j],
                #        'Autor_': autor_[j],
                #        'URL_':url_[j]
                #    }
                #    cursor.execute(query,data_)
                #    cnx.commit()
                #    print("Carga de articulo "+str(i)+"-"+str(j+1)+" Completa")

            except mysql.connector.Error as err:
                if err != -1:
                    print(err)
                else:
                    raise            

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    main()