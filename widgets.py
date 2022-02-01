import tkinter as tinker
from tkinter import RIGHT, ttk
from tkinter.constants import END
from databaseFunctions import noValueQuery

#Creates a label and entry
class labelEntryView():

    def __init__(self, location, row, column, labelText):

        self.label = tinker.Label(location, text=labelText).grid(row=row, column=column)
        self.entry = tinker.Entry(location)
        self.entry.grid(row=row, column=column+1)

    #get value of the entry
    def getEntryValue(self):

        return self.entry.get()

    #Replaces entry value
    def entryRowValue(self, start, text):

        self.entry.delete(start, END)
        self.entry.insert(start, text)

    #Delete entry Values
    def deleteEntryValue(self, start):

        self.entry.delete(start, END)

#Used to create a doule label
class doubleLabelView():

        def __init__(self, location, row, column, labelText):

            self.label = tinker.Label(location, text=labelText).grid(row=row, column=column)
            self.value = tinker.Label(location, text="")
            self.value.grid(row=row, column=column+1)

        #Get values of a label
        def getValue(self):
            return self.value.cget("text")

        #Changes value of a label
        def changeValue(self, newValue:str):
            self.value.config(text=newValue)

#used to create table
class tableView():

    def __init__(self, columnList: list, query: str, location: tinker.LabelFrame, columnWidth: int = 100):

        self.numColumns = len(columnList)
        self.table = ttk.Treeview(location, columns=columnList, show="headings")

        databaseData = noValueQuery(query)

        for i in range(len(columnList)):
            self.table.heading(columnList[i], text=columnList[i])
        
        for j in databaseData:
            self.table.insert('', END, values=j)

        for i in range(self.numColumns + 1):
            self.table.column('#' + str(i), width=columnWidth)

        #Scroll Bar
        self.yScroll = ttk.Scrollbar(location, orient="vertical", command=self.table.yview)
        self.yScroll.pack(side=RIGHT, fill="y")

        self.table.pack(pady=(10, 0))

        self.rows = "Number Of Data: " + self.getRows()
        self.rowCount = tinker.Label(location, text= self.rows)
        self.rowCount.pack()

    #Gets table
    def getTable(self):

        return self.table

    #Gets the rows items of a table
    def getRows(self):

        return str(len(self.table.get_children()))

    #Clears the table
    def clearTable(self):

        self.table.delete(*self.table.get_children())

    #Changes values of a table
    def changeTable(self, data):

        self.clearTable()

        for j in data:
            self.table.insert('', tinker.END, values=j)

        newText = "Number Of Data: " + self.getRows()
        self.rowCount.config(text=newText)

    

    

