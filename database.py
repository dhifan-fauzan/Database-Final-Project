import mysql.connector

#Variable used to connect to the database using mysql.connect
__myDatabase = mysql.connector.connect(

    host="sigma.jasoncoding.com",
    user="dhifan",
    passwd="databaseclass",
    database="dhifan_fauzan",
    port=5555
)   

#Get the database
def getDataBase():
    
    if not __myDatabase.is_connected():
        __myDatabase.reconnect()
    
    return __myDatabase