
from bs4 import BeautifulSoup
import urllib.request as url
import mysql.connector
from mysql.connector import errorcode

url_base_ = "https://elementos.buap.mx/num_single.php?num="
add_article_ = ("INSERT INTO numeros VALUES (%(Numero_)s, %(Num_Address_)s, %(Indice_)s);")

try:
    #cnx = mysql.connector.connect(user='root', password='123456',
    #                          host='127.0.0.1',
    #                          database='cd_elementos')
    #print(cnx)
    cursor = cnx.cursor()
    for i in range(50,51):
        ready_=False
        buff_ = ""
        indice_ = ""
        try:
            html_ = url.urlopen(url_base_+str(i))
            soup = BeautifulSoup(html_,'html.parser')
            print("html download succesfull from "+url_base_+str(i))
            print(len(soup))

            for tag in soup.find_all(True):
                if tag.name == 'button':
                    print(tag.string)
                   
            #indice_ = buff_[buff_.find("Inicio\nNúmeros anteriores\nA los autores\nDirectorio\nSuscripción\nContacto")+71:buff_.find("Número actual\n\n\n\n\n\n\n\n\n")]
            #for j in range(0,10):
            #    indice_ = indice_.replace("\n\n","\n")
            #    indice_ = indice_.replace("\t","")
            #    indice_ = indice_.replace("\r","")
            #    indice_ = indice_.replace("  "," ")
            
            #print("article data cleaning succesfull, article length:")
            #print(len(article_))

            article_data_ = {
                'Numero_' : i,
                'Num_Address_' : url_base_+str(i),
                'Indice_': indice_
                }
            
            print("ready for query")
            print(article_data_)

            #cursor.execute(add_article_,article_data_)
            #cnx.commit()
            #print("done")

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

cursor.close()
cnx.close()
