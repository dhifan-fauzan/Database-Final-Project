import database

dataBase = database.getDataBase()
databseCursor = dataBase.cursor()

#Funtion for inserting or deleting rows in a database
def insertAndDeleteDB(query: str, value: tuple):
    
    databseCursor.execute(query, value)
    dataBase.commit()

#Function mainly used for checking if a data exist in a table, it is also used to get single values
def valueExists(query:str, value: tuple):

    databseCursor.execute(query, value)
    databaseData = databseCursor.fetchall()

    return databaseData[0][0]

#Function for getting data from a database, without using any value. Mainly used for queries such as SELECT * FROM table
def noValueQuery(query):

    databseCursor.execute(query)
    databaseData = databseCursor.fetchall()

    return databaseData

#Function for getting data from a database, but using value for specific rows
def valueQuery(query, val):

    databseCursor.execute(query, val)
    databaseData = databseCursor.fetchall()

    return databaseData