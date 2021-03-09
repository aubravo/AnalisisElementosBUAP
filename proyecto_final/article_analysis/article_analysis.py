# -*- coding: utf-8 -*-

from proyecto_final.web_scrapper import web_scrapper
import re
import io

Words = set()
transTable = str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU")
query = ("SELECT ID,Contenido FROM articulos")

cnx, cursor= web_scrapper.mysql_connection()
cursor.execute(query)
cursor_buff = cursor.fetchall()

with io.open('stop_words.txt','r',encoding="utf-8") as stop_words:
    stop_words_ = stop_words.readline().split(',')

for (id,contenido) in cursor_buff:
    buff = re.sub('[^a-zA-Z]+',' ',contenido.translate(transTable)).lower().split(' ')
    Words = set(Words).union(set(buff))


print("REMOVING STOP WORDS")
for stop_ in stop_words_:
    try:
        Words.remove(stop_)
    except:
        print(stop_+" not in list")


query = ("INSERT INTO palabras VALUES (%(palabra_)s, %(ID_)s, %(repeticiones_)s);")
for (id,contenido) in cursor_buff:
    print("analyzing article "+str(id))
    buff = re.sub('[^a-zA-Z]+',' ',contenido.translate(transTable)).lower().split(' ')
    for word in Words:
        if word in buff:
            data_ = {
               "palabra_"       :   word,
               "ID_"            :   id,
               "repeticiones_"  :   buff.count(word)
            }
            cursor.execute(query,data_)
            cnx.commit()

cursor.close
cnx.close