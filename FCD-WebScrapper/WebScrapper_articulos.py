
from bs4 import BeautifulSoup
import urllib.request as url
import mysql.connector
from mysql.connector import errorcode

url_base_ = "https://elementos.buap.mx/post.php?id="
add_article_ = ("INSERT INTO articulos VALUES (%(Art_Num_)s, %(Address_)s, %(Articulo_)s);")

def main():
    try:
        cnx = mysql.connector.connect(user='root', password='123456',
                                  host='127.0.0.1',
                                  database='cd_elementos')
        print(cnx)
        cursor = cnx.cursor()
        for i in range(277,278):
            ready_=False
            buff_ = ""
            article_ = ""
            try:
                html_ = url.urlopen(url_base_+str(i))
                soup = BeautifulSoup(html_,'html.parser')
                print("html download succesfull from "+url_base_+str(i))
                print(len(soup))

                for tag in soup.find_all(True):
                    if tag.b and not ready_:
                        try:
                            for string in tag.strings:
                                buff_ += string
                        except:
                            pass
                        ready_ = True
                article_ = buff_[buff_.find("Inicio\nNúmeros anteriores\nA los autores\nDirectorio\nSuscripción\nContacto")+71:buff_.find("Número actual\n\n\n\n\n\n\n\n\n")]
                for j in range(0,10):
                    article_ = article_.replace("\n\n","\n")
                    article_ = article_.replace("\t","")
                    article_ = article_.replace("\r","")
                    article_ = article_.replace("  "," ")
            
                print("article data cleaning succesfull, article length:")
                print(len(article_))

                article_data_ = {
                    'Art_Num_' : i,
                    'Address_' : url_base_+str(i),
                    'Articulo_': article_
                    }
            
                print("ready for query")

                cursor.execute(add_article_,article_data_)
                cnx.commit()
                print("done")

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


if __name__ == "__main__":
    main()