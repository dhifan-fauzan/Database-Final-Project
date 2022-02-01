import database

dataBase = database.getDataBase()
databseCursor = dataBase.cursor()

def insertAndDeleteDB(query: str, value: tuple):
    
    databseCursor.execute(query, value)
    dataBase.commit()

def valueExists(query:str, value: tuple):

    databseCursor.execute(query, value)
    databaseData = databseCursor.fetchall()

    return databaseData[0][0]

def noValueQuery(query):

    databseCursor.execute(query)
    databaseData = databseCursor.fetchall()

    return databaseData

def valueQuery(query, val):

    databseCursor.execute(query, val)
    databaseData = databseCursor.fetchall()

    return databaseData