import mysql.connector

__myDatabase = mysql.connector.connect(

    host="sigma.jasoncoding.com",
    user="dhifan",
    passwd="databaseclass",
    database="dhifan_fauzan",
    port=5555
)   

def getDataBase():
    
    if not __myDatabase.is_connected():
        __myDatabase.reconnect()
    
    return __myDatabase