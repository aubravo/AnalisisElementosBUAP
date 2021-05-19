# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

def connect(**params_):
    try:
        cnx = mysql.connector.connect(user  = params_["user"],
                                  password  = params_["password"],
                                  host      = params_["host"],
                                  database  = params_["database"]
                                  )
        cursor = cnx.cursor()
        return cnx, cursor
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuario o contrasena incorrectos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)

if __name__ == "__main__" :
    cnx,cursor = mysql_connection( user = "root", password = "123456", host = "127.0.0.1", database = "cd_elementos" )
    print (cnx)

