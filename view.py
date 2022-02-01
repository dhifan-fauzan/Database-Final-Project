from databaseFunctions import insertAndDeleteDB, noValueQuery, valueQuery, valueExists
from datetime import date
import tkinter as tinker
from tkinter import messagebox
from widgets import labelEntryView, doubleLabelView, tableView


class Application(tinker.Tk):
    
    def __init__(self):
        
        tinker.Tk.__init__(self)
        
        self.frame = None
        self.switchFrame(mainMenu)

    #Function used to switch between various Windows
    def switchFrame(self, nFrame):

        newFrame = nFrame(self)

        if self.frame is not None:
            self.frame.destroy()

        self.frame = newFrame
        self.frame.pack()

#MainMenu Class
class mainMenu(tinker.Frame):
    
    def __init__(self, master):
        
        tinker.Frame.__init__(self, master)

        self.master = master

        self.companyTitle= tinker.Label(
            self, text="Green Company",
            font = ("Arial",30) )
        self.companyTitle.grid(row=1, column=0, columnspan=3)

        self.introTitle = tinker.Label(
            self, text = "Choose a Menu",)
        self.introTitle.grid(row=2, column=0, columnspan=3)

        #Buttons 
        #Button to access Branch Table
        self.branchButton = tinker.Button(self, text = "Branch", 
                                        command = lambda: self.master.switchFrame(branch),
                                        height= 10, width=30)
        self.branchButton.grid(row=3,column=0)

        #Button to access Products Table
        self.productsButton = tinker.Button(self, text = "Products", 
                                            command = lambda: self.master.switchFrame(product),
                                            height= 10, width=30)
        self.productsButton.grid(row=3,column=1)

        #Button to access Customers Table
        self.customerButton = tinker.Button(self, text = "Customers", 
                                            command = lambda: self.master.switchFrame(customer),
                                            height= 10, width=30)
        self.customerButton.grid(row=3,column=2)

        #Button to access Employees Table
        self.employeesButton = tinker.Button(self, text = "Employees", 
                                            command = lambda: self.master.switchFrame(employee),
                                            height= 10, width=30)
        self.employeesButton.grid(row=4,column=0)

        #Button to access Inventory Table
        self.inventoryButton = tinker.Button(self, text = "Inventory", 
                                            command = lambda: self.master.switchFrame(stock),
                                            height= 10, width=30)
        self.inventoryButton.grid(row=4,column=1)
        
        #Button to access Sales Table
        self.salesButton = tinker.Button(self, text = "Sales", 
                                            command = lambda: self.master.switchFrame(sales),
                                            height= 10, width=30)
        self.salesButton.grid(row=4,column=2)

class branch(tinker.Frame):
    
    def __init__(self, master):
        
        tinker.Frame.__init__(self, master)

        #Column Headings for table
        self.columnHeading = ["Id", "Name", "Street", "City", "State"]

        #Wrapers to place the different button, entries and labels
        self.searchWraper = tinker.LabelFrame(self,  text="Search")
        self.dataWraper = tinker.LabelFrame(self,  text="Form")
        self.tableWraper = tinker.LabelFrame(self, text="Branch Table")
 
        self.tableWraper.pack(fill="both", expand="yes", padx=20)
        
        #Creating Branch Table
        self.branchQuery = "SELECT * FROM Branch"
        self.branchTable = tableView(self.columnHeading, self.branchQuery, self.tableWraper)
        #Binding Double Click to place data from table to their respective entries and labels
        self.branchTable.getTable().bind("<Double 1>", self.getRowValue)

        #Search Warper
        self.searchWraper.pack(fill="both", expand="yes", padx=20)
        self.searchBlock = labelEntryView(self.searchWraper, 0, 0, "Branch No:")

        self.searchButton = tinker.Button(self.searchWraper, command=self.searchId , text="Search")
        self.searchButton.grid(row=0, column=2)

        self.stateBlock = labelEntryView(self.searchWraper, 1, 0, "State:")
        self.searchStateButton = tinker.Button(self.searchWraper, command=self.searchState , text="Search")
        self.searchStateButton.grid(row=1, column=2)

        self.blockList = [self.searchBlock, self.stateBlock]

        self.resetButton = tinker.Button(self.searchWraper, command=self.resetTable , text="Reset")
        self.resetButton.grid(row=2, column=2)

        #Data Wrapper

            #Labels and Entries
        self.dataWraper.pack(fill="both", expand="yes", padx=20)
        self.branchId = doubleLabelView(self.dataWraper, 0, 0, "Branch Id:")
        self.branchName = labelEntryView(self.dataWraper, 1, 0, "Branch Name:")
        self.street = labelEntryView(self.dataWraper, 2, 0, "Street:")
        self.city = labelEntryView(self.dataWraper, 3, 0, "City:")
        self.state = labelEntryView(self.dataWraper, 4, 0, "State:")

            #Buttons
        self.insertButton = tinker.Button(self.dataWraper, text="Insert", command=self.insertValues)
        self.insertButton.grid(row=5, column=0)
        
        self.deleteButton = tinker.Button(self.dataWraper, text="Delete", command=self.deleteValues)
        self.deleteButton.grid(row=5, column=1)

        self.clearButton = tinker.Button(self.dataWraper, text="Clear Selected Data", command=self.clearValues)
        self.clearButton.grid(row=5, column=2)

        self.listLabel = [self.branchId,]
        self.listEntries = [self.branchName, self.street, self.city, self.state]

        self.mainMenu = tinker.Button(self, text="Main Menu", command=lambda: self.master.switchFrame(mainMenu))
        self.mainMenu.pack()

    #Clear All Values from Entries and Labels
    def clearValues(self):

        self.branchId.changeValue("")

        for o in self.blockList:
            o.deleteEntryValue(0)

        for i in self.listEntries:
            i.deleteEntryValue(0)

    #Updates the table based on query
    def updateTable(self, query):

        self.clearValues()

        newData = noValueQuery(query)

        self.branchTable.changeTable(newData)

    #Reverts back table to original State
    def resetTable(self):

        self.updateTable(self.branchQuery)
        self.searchBlock.deleteEntryValue(0)

    #Used to Search for data based on the branchNo
    def searchId(self):

        value = self.searchBlock.getEntryValue()

        #Validates the value entered to avoid error
        if  value != "" and value.isdecimal():

            idQuery = self.branchQuery + " WHERE branchNo=%s"
            value = int(value)

            databaseData = valueQuery(idQuery, (value,))

            self.branchTable.changeTable(databaseData)
            self.searchBlock.deleteEntryValue(0)

        else:
            messagebox.showwarning(title="Error", message="Invalid Branch No for search")

    #Used to search for data based on the State
    def searchState(self):

        value = self.stateBlock.getEntryValue()

        #Validates the value entered to avoid error
        if value != "":

            stateQuery = self.branchQuery + " WHERE state LIKE '%" + value + "%'"
            self.updateTable(stateQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid State for search")

    #Places Table Values to Entries And Labels
    def getRowValue(self, event):

        table = self.branchTable.getTable()
        
        rowId = table.identify_row(event.y)
        rowItems = table.item(table.focus())

        self.branchId.changeValue(rowItems["values"][0])

        for i, o in enumerate(self.listEntries, 1):
            
            o.entryRowValue(0, rowItems["values"][i])

    #Used to insert a new row into the database
    def insertValues(self):
        
        inputs = tuple()

        for i in self.listEntries:
            
            inputs += (i.getEntryValue(),)

        #Insert Query
        insertQuery = "INSERT INTO Branch (branchName, street, city, state) VALUES (%s, %s, %s, %s)"

        #Inserting and Updating the table
        insertAndDeleteDB(insertQuery, inputs)
        self.updateTable(self.branchQuery)

    #Used to delete data from a table
    def deleteValues(self):
 
        deleteValue = (int(self.branchId.getValue()),)

        #Used to Check if data is used in another table
        existQuery = "SELECT EXISTS(SELECT * FROM Employees WHERE branchNo=%s)"
        numberOfUse = valueExists(existQuery, deleteValue)

        existStock = "SELECT EXISTS(SELECT * FROM Stock WHERE branchNo=%s)"
        numberOfUse += valueExists(existStock, deleteValue)

        existSales = "SELECT EXISTS(SELECT * FROM Sales WHERE branchNo=%s)"
        numberOfUse += valueExists(existSales, deleteValue)

        #Ensures that if data is used it cannot be deleted
        if numberOfUse == 0:

            deleteQeury = "DELETE FROM Branch WHERE branchNo=%s"
            insertAndDeleteDB(deleteQeury, deleteValue)
            self.updateTable(self.branchQuery)

        else:
            messagebox.showwarning(title="Error", message="This Value is used in Another Table")

class product(tinker.Frame):
    
    def __init__(self, master):
        
        tinker.Frame.__init__(self, master)

        #Used for table columns
        self.columnHeading = ["Id", "Name", "Type", "Price"]

        #Used to store buttons, entries and Labels
        self.searchWraper = tinker.LabelFrame(self,  text="Search")
        self.dataWraper = tinker.LabelFrame(self,  text="Form")
        self.tableWraper = tinker.LabelFrame(self, text="Products Table")
 
        self.tableWraper.pack(fill="both", expand="yes", padx=20)
        #Query for table
        self.productQuery = "SELECT * FROM Products"
        #Creating the table
        self.productTable = tableView(self.columnHeading, self.productQuery, self.tableWraper, 150)
        self.productTable.getTable().bind("<Double 1>", self.getRowValue)

        #Search Warper
        self.searchWraper.pack(fill="both", expand="yes", padx=20)
        #Labels And Entries For Search Buttons
        self.searchBlock = labelEntryView(self.searchWraper, 0, 0, "Product Id:")
        self.typeBlock = labelEntryView(self.searchWraper, 1, 0, "Product Type:")

        self.blockList = [self.searchBlock, self.typeBlock]

        #Search Buttons
        self.searchButton = tinker.Button(self.searchWraper, command=self.searchId , text="Search")
        self.searchButton.grid(row=0, column=2)

        self.typeButton = tinker.Button(self.searchWraper, command=self.searchType , text="Search")
        self.typeButton.grid(row = 1, column= 2)

        self.resetButton = tinker.Button(self.searchWraper, command=self.resetTable , text="Reset")
        self.resetButton.grid(row=2, column=2)

        #Data Wrapper
        self.dataWraper.pack(fill="both", expand="yes", padx=20)
        self.productId = doubleLabelView(self.dataWraper, 0, 0, "Product Id:")
        self.productName = labelEntryView(self.dataWraper, 1, 0, "Name:")
        self.type = labelEntryView(self.dataWraper, 2, 0, "Type:")
        self.price = labelEntryView(self.dataWraper, 3, 0, "Price:")

        self.insertButton = tinker.Button(self.dataWraper, text="Insert", command=self.insertValues)
        self.insertButton.grid(row=5, column=0)
        
        self.deleteButton = tinker.Button(self.dataWraper, text="Delete", command=self.deleteValues)
        self.deleteButton.grid(row=5, column=1)

        self.clearButton = tinker.Button(self.dataWraper, text="Clear Selected Data", command=self.clearValues)
        self.clearButton.grid(row=5, column=2)

        self.listLabel = [self.productId,]
        self.listEntries = [self.productName, self.type, self.price]

        self.mainMenu = tinker.Button(self, text="Main Menu", command=lambda: self.master.switchFrame(mainMenu))
        self.mainMenu.pack()

    #Clear all Values in entries and Labels
    def clearValues(self):

        self.productId.changeValue("")

        for o in self.blockList:
            o.deleteEntryValue(0)

        for i in self.listEntries:
            
            i.deleteEntryValue(0)

    #Used to update table based on Query
    def updateTable(self, query):

        self.clearValues()
        newData = noValueQuery(query)
        self.productTable.changeTable(newData)

    #Resets the table back to its original State
    def resetTable(self):

        self.updateTable(self.productQuery)
        self.searchBlock.deleteEntryValue(0)

    #Used to search based on product id
    def searchId(self):

        value = self.searchBlock.getEntryValue()

        if  value != "" and value.isdecimal():

            idQuery = self.productQuery + " WHERE productId=%s"
            value = int(value)
            databaseData = valueQuery(idQuery, (value,))
            self.productTable.changeTable(databaseData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Branch No for search")

    #Used to search based on product type
    def searchType(self):

        value = self.typeBlock.getEntryValue()

        if value != "":

            typeQuery = self.productQuery + " WHERE type LIKE '%" + value + "%'"
            self.updateTable(typeQuery)
        
        else:

            messagebox.showwarning(title="Error", message="Invalid Product Type for search")

    #Used to get Values from table into entries and labels
    def getRowValue(self, event):

        table = self.productTable.getTable()
        
        rowId = table.identify_row(event.y)
        rowItems = table.item(table.focus())

        self.productId.changeValue(rowItems["values"][0])

        for i, o in enumerate(self.listEntries, 1):
            
            o.entryRowValue(0, rowItems["values"][i])

    #Used to Insert Values into database
    def insertValues(self):
        
        inputs = tuple()

        for i in self.listEntries:
            
            inputs += (i.getEntryValue(),)

        #Validation to avoid error.
        if inputs[2].replace('.','',1).isdigit():

            insertQuery = "INSERT INTO Products (name, type, price) VALUES (%s, %s, %s)"

            #Inserts into database and update the table
            insertAndDeleteDB(insertQuery, inputs)
            self.updateTable(self.productQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid Price")

    #Used to Delete Values from a database
    def deleteValues(self):
        
        deleteValue = (int(self.productId.getValue()),)

        existQuery = "SELECT EXISTS(SELECT * FROM Stock WHERE productID=%s)"
        numberOfUse = valueExists(existQuery, deleteValue)

        existQuery = "SELECT EXISTS(SELECT * FROM Sales WHERE productId=%s)"
        numberOfUse += valueExists(existQuery, deleteValue)

        #Ensure that if a data is used in another table it does not get deleted
        if numberOfUse == 0:

            deleteQuery = "DELETE FROM Products WHERE productID=%s"
            insertAndDeleteDB(deleteQuery, deleteValue)
            self.updateTable(self.productQuery)

        else:
            messagebox.showwarning(title="Error", message="This Value is used in Another Table")

class customer(tinker.Frame):
    
    def __init__(self, master):
        
        tinker.Frame.__init__(self, master)

        #Table headings
        self.columnHeading = ["Id", "First Name", "Last Name", "Phone No."]

        self.searchWraper = tinker.LabelFrame(self,  text="Search")
        self.dataWraper = tinker.LabelFrame(self,  text="Form")
        self.tableWraper = tinker.LabelFrame(self, text="Customers Table")
 
        self.tableWraper.pack(fill="both", expand="yes", padx=20)
        self.customerQuery = "SELECT * FROM Customers"
        #Creating Table
        self.customerTable = tableView(self.columnHeading, self.customerQuery, self.tableWraper)
        self.customerTable.getTable().bind("<Double 1>", self.getRowValue)

        #Search Warper
        self.searchWraper.pack(fill="both", expand="yes", padx=20)
        self.searchBlock = labelEntryView(self.searchWraper, 0, 0, "Customer Id:")
        self.nameBlock = labelEntryView(self.searchWraper, 1, 0, "Customer Name:")

        self.blockList = [self.searchBlock, self.nameBlock]

        self.searchButton = tinker.Button(self.searchWraper, command=self.searchId , text="Search")
        self.searchButton.grid(row=0, column=2)

        self.nameButton = tinker.Button(self.searchWraper, command=self.searchName, text="Search")
        self.nameButton.grid(row=1, column=2)

        self.resetButton = tinker.Button(self.searchWraper, command=self.resetTable , text="Reset")
        self.resetButton.grid(row=2, column=2)

        #Data Wrapper
        self.dataWraper.pack(fill="both", expand="yes", padx=20)
        self.customerId = doubleLabelView(self.dataWraper, 0, 0, "Customer Id:")
        self.firstName = labelEntryView(self.dataWraper, 1, 0, "First Name:")
        self.lastName = labelEntryView(self.dataWraper, 2, 0, "Last Name:")
        self.number = labelEntryView(self.dataWraper, 3, 0, "Phone No.:")

        self.insertButton = tinker.Button(self.dataWraper, text="Insert", command=self.insertValues)
        self.insertButton.grid(row=5, column=0)
        
        self.deleteButton = tinker.Button(self.dataWraper, text="Delete", command=self.deleteValues)
        self.deleteButton.grid(row=5, column=1)

        self.clearButton = tinker.Button(self.dataWraper, text="Clear Selected Data", command=self.clearValues)
        self.clearButton.grid(row=5, column=2)

        self.listLabel = [self.customerId,]
        self.listEntries = [self.firstName, self.lastName, self.number]

        self.mainMenu = tinker.Button(self, text="Main Menu", command=lambda: self.master.switchFrame(mainMenu))
        self.mainMenu.pack()

    #Used to Clear entries and labels
    def clearValues(self):

        self.customerId.changeValue("")

        for j in self.blockList:
            j.deleteEntryValue(0)

        for i in self.listEntries:
            
            i.deleteEntryValue(0)

    #Used to Update Table
    def updateTable(self, query):

        self.clearValues()
        newData = noValueQuery(query)
        self.customerTable.changeTable(newData)

    #Resets table
    def resetTable(self):

        self.updateTable(self.customerQuery)
        self.searchBlock.deleteEntryValue(0)

    #Search based on Customer Id
    def searchId(self):

        value = self.searchBlock.getEntryValue()

        if  value != "" and value.isdecimal():

            idQuery = self.customerQuery + " WHERE customerID=%s"
            value = int(value)

            databaseData = valueQuery(idQuery, (value,))

            self.customerTable.changeTable(databaseData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Customer Id for search")

    #Search based on Customer Name
    def searchName(self):

        value = self.nameBlock.getEntryValue()

        if  value != "":

            nameQuery = self.customerQuery + " WHERE firstName LIKE '%" + value + "%' or lastName LIKE '%" + value + "%'"
            self.updateTable(nameQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid Customer Name for search")

    #Used to get data from table and insert into entries and labels
    def getRowValue(self, event):

        table = self.customerTable.getTable()
        
        rowId = table.identify_row(event.y)
        rowItems = table.item(table.focus())

        self.customerId.changeValue(rowItems["values"][0])

        for i, o in enumerate(self.listEntries, 1):
            
            o.entryRowValue(0, rowItems["values"][i])

    #Insert values into database
    def insertValues(self):
        
        inputs = tuple()

        for i in self.listEntries:
            
            inputs += (i.getEntryValue(),)

        insertQuery = "INSERT INTO Customers (firstName, lastName, phoneNo) VALUES (%s, %s, %s)"

        #Validaing the value to avoid errors
        if len(inputs[2]) == 8 and inputs[2].isdecimal:

            insertAndDeleteDB(insertQuery, inputs)

            self.updateTable(self.customerQuery)
        
        else:
            messagebox.showwarning(title="Error", message="Invalid Phone Number")

    def deleteValues(self):
        
        deleteValue = (int(self.customerId.getValue()),)

        existQuery = "SELECT EXISTS(SELECT * FROM Sales WHERE customerID=%s)"
        numberOfUse = valueExists(existQuery, deleteValue)

        if numberOfUse == 0:
            deleteQeury = "DELETE FROM Customers WHERE customerID=%s"
            insertAndDeleteDB(deleteQeury, deleteValue)
            self.updateTable(self.customerQuery)

        else:
            messagebox.showwarning(title="Error", message="Value Used in Another Table")

class employee(tinker.Frame):
    
    def __init__(self, master):
        
        tinker.Frame.__init__(self, master)

        #Used For Table Column Headings
        self.columnHeading = ["Id", "First Name", "Last Name", "Position", "Gender", "Age", "Branch No", "Branch Name"]

        self.searchWraper = tinker.LabelFrame(self,  text="Search")
        self.dataWraper = tinker.LabelFrame(self,  text="Form")
        self.tableWraper = tinker.LabelFrame(self, text="Employees Table")
 
        self.tableWraper.pack(fill="both", expand="yes", padx=20) 
        self.employeesQuery = "SELECT emp.employeeID, emp.firstName, emp.lastName, emp.position, emp.gender, emp.age, br.branchNo, br.branchName FROM Employees as emp JOIN Branch as br ON emp.branchNo=br.branchNo"
        #Used to Create the table
        self.employeesTable = tableView(self.columnHeading, self.employeesQuery, self.tableWraper)
        self.employeesTable.getTable().bind("<Double 1>", self.getRowValue)

        #Exist Query 
        self.branchExistQuery = "SELECT EXISTS(SELECT * FROM Branch WHERE branchNo=%s)"

        #Search Warper
        self.searchWraper.pack(fill="both", expand="yes", padx=20)
        self.searchBlock = labelEntryView(self.searchWraper, 0, 0, "Employee Id:")
        self.nameBlock = labelEntryView(self.searchWraper, 1, 0, "Employee Name:")
        self.genderBlock = labelEntryView(self.searchWraper, 2, 0, "Gender:")
        self.positionBlock = labelEntryView(self.searchWraper, 0, 3, "Position:")
        self.branchBlock = labelEntryView(self.searchWraper, 1, 3, "Branch Id:")

        self.blockList = [self.searchBlock, self.nameBlock, self.genderBlock, self.positionBlock, self.branchBlock]

        self.searchButton = tinker.Button(self.searchWraper, command=self.searchId , text="Search")
        self.searchButton.grid(row=0, column=2)

        self.nameButton = tinker.Button(self.searchWraper, command=self.searchName , text="Search")
        self.nameButton.grid(row=1, column=2)

        self.genderButton = tinker.Button(self.searchWraper, command=self.searchGender , text="Search")
        self.genderButton.grid(row=2, column=2)

        self.positionButton = tinker.Button(self.searchWraper, command=self.searchPosition , text="Search")
        self.positionButton.grid(row=0, column=5)

        self.branchButton = tinker.Button(self.searchWraper, command=self.searchBranch , text="Search")
        self.branchButton.grid(row=1, column=5)

        self.resetButton = tinker.Button(self.searchWraper, command=self.resetTable , text="Reset")
        self.resetButton.grid(row=3, column=2)

        #Data Wrapper
        self.dataWraper.pack(fill="both", expand="yes", padx=20)
        self.employeesId = doubleLabelView(self.dataWraper, 0, 0, "Customer Id:")
        self.firstName = labelEntryView(self.dataWraper, 1, 0, "First Name:")
        self.lastName = labelEntryView(self.dataWraper, 2, 0, "Last Name:")
        self.position = labelEntryView(self.dataWraper, 3, 0, "Position:")
        self.gender = labelEntryView(self.dataWraper, 4, 0, "Gender:")
        self.age = labelEntryView(self.dataWraper, 5, 0, "Age:")
        self.branchNo = labelEntryView(self.dataWraper, 0, 2, "Branch Id:")
        self.branchName = doubleLabelView(self.dataWraper, 1, 2, "Branch Name:")

        self.insertButton = tinker.Button(self.dataWraper, text="Insert", command=self.insertValues)
        self.insertButton.grid(row=6, column=0)
        
        self.deleteButton = tinker.Button(self.dataWraper, text="Delete", command=self.deleteValues)
        self.deleteButton.grid(row=6, column=1)

        self.clearButton = tinker.Button(self.dataWraper, text="Clear Selected Data", command=self.clearValues)
        self.clearButton.grid(row=6, column=2)

        self.checkBranchbutton = tinker.Button(self.dataWraper, text="Check", command=self.checkBranch)
        self.checkBranchbutton.grid(row=0, column=4)

        self.listLabel = [self.employeesId, self.branchName]
        self.listEntries = [self.firstName, self.lastName, self.position, self.gender, self.age, self.branchNo]

        self.mainMenu = tinker.Button(self, text="Main Menu", command=lambda: self.master.switchFrame(mainMenu))
        self.mainMenu.pack()

    #Used to clear entires and labels
    def clearValues(self):

        for o in self.blockList:
            o.deleteEntryValue(0)

        for i in self.listLabel:
            i.changeValue("")

        for j in self.listEntries:
            j.deleteEntryValue(0)

    #Used to update the Table
    def updateTable(self, query):

        self.clearValues()

        newData = noValueQuery(query)

        self.employeesTable.changeTable(newData)

    #Used to reset the table to original form
    def resetTable(self):

        self.updateTable(self.employeesQuery)
        self.searchBlock.deleteEntryValue(0)

    #Search Based on Employee ID
    def searchId(self):

        value = self.searchBlock.getEntryValue()

        if value != "" and value.isdecimal():

            idQuery = self.employeesQuery + " WHERE employeeID=%s"
            value = int(value)

            newData = valueQuery(idQuery, (value,))

            self.employeesTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Employees Id for search")

    #Search Based on employee Name
    def searchName(self):

        value = self.nameBlock.getEntryValue()

        if value != "":

            nameQuery = self.employeesQuery + " WHERE firstName LIKE '%" + value + "%' or lastName LIKE '%" + value + "%'"
            self.updateTable(nameQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid Employee Name for search")

    #Search based on employees gender
    def searchGender(self):
        
        value = self.genderBlock.getEntryValue()
        acceptablegender = ["Male", "Female"]

        if value != "" and value in acceptablegender:

            genderQuery = self.employeesQuery + " WHERE gender=%s"
            data = valueQuery(genderQuery, (value,))
            self.employeesTable.changeTable(data)

        else:
            messagebox.showwarning(title="Error", message="Invalid Gender for search")

    #search based on employees position
    def searchPosition(self):

        value = self.positionBlock.getEntryValue()

        if value != "":
            positionQuery = self.employeesQuery + " WHERE position LIKE '%" + value + "%'"
            self.updateTable(positionQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid Employee Position for search")

    #Search based on the branch they work at
    def searchBranch(self):
        
        value = self.branchBlock.getEntryValue()

        if value != "" and value.isdecimal():
            idBQuery = self.employeesQuery + " WHERE br.branchNo=%s"
            value = int(value)
            newData = valueQuery(idBQuery, (value,))
            self.employeesTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Branch No. for search")

    #Places table values into entries and labels
    def getRowValue(self, event):

        table = self.employeesTable.getTable()
        
        rowId = table.identify_row(event.y)
        rowItems = table.item(table.focus())

        self.employeesId.changeValue(rowItems["values"][0])
        self.branchName.changeValue(rowItems["values"][7])

        for i, o in enumerate(self.listEntries, 1):
            
            o.entryRowValue(0, rowItems["values"][i])

    #Used to check if a branch no exists
    def checkBranch(self):
        
        value = self.branchNo.getEntryValue()

        if value != "":

            exist = valueExists(self.branchExistQuery, (int(value),))

            if exist > 0:
                searchQuery = "SELECT branchName FROM Branch WHERE branchNo=%s"
                branchName = valueExists(searchQuery, (value,))

                self.branchName.changeValue(branchName)

            else:
                self.branchName.changeValue("null")

    #Insert into database
    def insertValues(self):
        
        inputs = tuple()

        for i in self.listEntries:
            inputs += (i.getEntryValue(),)

        addQuery = "INSERT INTO Employees (firstName, lastName, position, gender, age, branchNo) VALUES (%s, %s, %s, %s, %s, %s)"

        exist = valueExists(self.branchExistQuery, (inputs[-1],))

        #Validation to ensure that only existing branch are inputted
        if exist > 0:

            insertAndDeleteDB(addQuery, inputs)
            self.updateTable(self.employeesQuery)
        
        else:
            messagebox.showwarning(title="Error", message="Invalid Branch Number")

    #Deletes values from database
    def deleteValues(self):
        
        deleteValue = self.employeesId.getValue()

        if deleteValue != "":

            deleteValue = (deleteValue,)
            deleteQuery = "Delete FROM Employees where employeeID=%s"
            insertAndDeleteDB(deleteQuery, deleteValue)
            self.updateTable(self.employeesQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid Employees ID for Deletion")

class stock(tinker.Frame):
    
    def __init__(self, master):
        
        tinker.Frame.__init__(self, master)

        #Talbe column headings
        self.columnHeading = ["Stock Id", "Product Id", "Product Name", "Product Type", "Branch No.", "Branch Name", "Quantity"]

        self.searchWraper = tinker.LabelFrame(self,  text="Search")
        self.dataWraper = tinker.LabelFrame(self,  text="Form")
        self.tableWraper = tinker.LabelFrame(self, text="Stocks Table")
 
        self.tableWraper.pack(fill="both", expand="yes", padx=20) 
        self.stockQuery = "SELECT stk.stockId, pd.productID, pd.name, pd.type, br.branchNo, br.branchName, stk.stock FROM Stock AS stk JOIN Products AS pd ON stk.productID=pd.productId JOIN Branch AS br ON br.branchNo=stk.branchNo"
        #Creating the table
        self.stockTable = tableView(self.columnHeading, self.stockQuery, self.tableWraper, 150)
        self.stockTable.getTable().bind("<Double 1>", self.getRowValue)

        self.branchExistQuery = "SELECT EXISTS(SELECT * FROM Branch WHERE branchNo=%s)"
        self.productExistQuery = "SELECT EXISTS(SELECT * FROM Products WHERE productId=%s)"

        #Search Warper
        self.searchWraper.pack(fill="both", expand="yes", padx=20)
        self.searchBlock = labelEntryView(self.searchWraper, 0, 0, "Stock Id:")
        self.branchBlock = labelEntryView(self.searchWraper, 1, 0, "Branch No:")
        self.productBlock = labelEntryView(self.searchWraper, 0, 3, "Product Id:")
        self.typeBlock = labelEntryView(self.searchWraper, 1, 3, "Product Type:")

        self.searchButton = tinker.Button(self.searchWraper, command=self.searchId , text="Search")
        self.searchButton.grid(row=0, column=2)

        self.branchButton = tinker.Button(self.searchWraper, command=self.searchBranch , text="Search")
        self.branchButton.grid(row=1, column=2)

        self.productButton = tinker.Button(self.searchWraper, command=self.searchProduct , text="Search")
        self.productButton.grid(row=0, column=5)

        self.typeButton = tinker.Button(self.searchWraper, command=self.searchType , text="Search")
        self.typeButton.grid(row=1, column=5)

        self.resetButton = tinker.Button(self.searchWraper, command=self.resetTable , text="Reset")
        self.resetButton.grid(row=2, column=2)

        self.blockList = [self.searchBlock, self.branchBlock, self.productBlock, self.typeBlock]

        #Data Wrapper
        self.dataWraper.pack(fill="both", expand="yes", padx=20)
        self.stockId = doubleLabelView(self.dataWraper, 0, 0, "Stock Id:")
        self.productId = labelEntryView(self.dataWraper, 1, 0, "Product Id:")
        self.productName = doubleLabelView(self.dataWraper, 2, 0, "Product Name:")
        self.productType = doubleLabelView(self.dataWraper, 3, 0, "Product Type:")
        self.quantity = labelEntryView(self.dataWraper, 4, 0, "Quantity:")
        self.branchNo = labelEntryView(self.dataWraper, 0, 3, "Branch Id:")
        self.branchName = doubleLabelView(self.dataWraper, 1, 3, "Branch Name:")

        self.insertButton = tinker.Button(self.dataWraper, text="Insert", command=self.insertValues)
        self.insertButton.grid(row=5, column=0)
        
        self.deleteButton = tinker.Button(self.dataWraper, text="Delete", command=self.deleteValues)
        self.deleteButton.grid(row=5, column=1)

        self.clearButton = tinker.Button(self.dataWraper, text="Clear Selected Data", command=self.clearValues)
        self.clearButton.grid(row=5, column=2)

        self.checkProductbutton = tinker.Button(self.dataWraper, text="Check", command=self.checkProduct)
        self.checkProductbutton.grid(row=1, column=2)

        self.checkBranchbutton = tinker.Button(self.dataWraper, text="Check", command=self.checkBranch)
        self.checkBranchbutton.grid(row=0, column=5)

        self.listLabel = [self.stockId, self.productName, self.productType, self.branchName]
        self.listEntries = [self.productId, self.branchNo, self.quantity]

        self.mainMenu = tinker.Button(self, text="Main Menu", command=lambda: self.master.switchFrame(mainMenu))
        self.mainMenu.pack()

    #Clear values from entries and labels
    def clearValues(self):

        for o in self.blockList:
            o.deleteEntryValue(0)

        for i in self.listLabel:
            i.changeValue("")

        for j in self.listEntries:
            j.deleteEntryValue(0)

    #Updates the table
    def updateTable(self, query):

        self.clearValues()

        newData = noValueQuery(query)

        self.stockTable.changeTable(newData)

    #Resets the table
    def resetTable(self):

        self.updateTable(self.stockQuery)
        self.searchBlock.deleteEntryValue(0)

    #Search based on stock id
    def searchId(self):

        value = self.searchBlock.getEntryValue()

        if value != "" and value.isdecimal():

            idQuery = self.stockQuery + " WHERE stockId=%s"
            value = int(value)
            newData = valueQuery(idQuery, (value,))
            self.stockTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Stock Id for search")

    #Search based on the branch
    def searchBranch(self):

        value = self.branchBlock.getEntryValue()

        if value != "" and value.isdecimal():

            idQuery = self.stockQuery + " WHERE br.branchNo=%s"
            value = int(value)
            newData = valueQuery(idQuery, (value,))
            self.stockTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Branch No for search")

    #Search based on the product id
    def searchProduct(self):
        
        value = self.productBlock.getEntryValue()

        if value != "" and value.isdecimal():

            idQuery = self.stockQuery + " WHERE pd.productID=%s"
            value = int(value)
            newData = valueQuery(idQuery, (value,))
            self.stockTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Product Id for search")

    #search based on the product type
    def searchType(self):
        
        value = self.typeBlock.getEntryValue()

        if value != "":

            idQuery = self.stockQuery + " WHERE pd.type=%s"
            newData = valueQuery(idQuery, (value,))
            self.stockTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Product Id for search")

    #Insert values from table into entries and labels
    def getRowValue(self, event):

        table = self.stockTable.getTable()
        
        rowId = table.identify_row(event.y)
        rowItems = table.item(table.focus())

        entriesValue = [1, 4, 6]
        labelValue = [0, 2, 3, 5]

        for i in range(3):
            
            self.listEntries[i].entryRowValue(0, rowItems["values"][entriesValue[i]])
            self.listLabel[i].changeValue(rowItems["values"][labelValue[i]])

        self.branchName.changeValue(rowItems["values"][labelValue[3]])

    #Checks if a branch exists
    def checkBranch(self):

        value =self.branchNo.getEntryValue()

        if value != "":

            exist = valueExists(self.branchExistQuery, (int(value),))

            if exist > 0:

                searchQuery = "SELECT branchName FROM Branch WHERE branchNo=%s"
                branchName = valueExists(searchQuery, (value,))
                self.branchName.changeValue(branchName)

            else:
                self.branchName.changeValue("null")

    #Checks if a product exists
    def checkProduct(self):

        value =self.productId.getEntryValue()

        if value != "":

            exist = valueExists(self.productExistQuery, (int(value),))

            if exist > 0:

                searchQuery = "SELECT name, type FROM Products WHERE productId=%s"
                branchName = valueQuery(searchQuery, (value,))
                self.productName.changeValue(branchName[0][0])
                self.productType.changeValue(branchName[0][1])

            else:
                self.productName.changeValue("null")
                self.productType.changeValue("null")

    #Inserts Value into database
    def insertValues(self):
        
        inputs = tuple()

        for i in self.listEntries:
            inputs += (i.getEntryValue(),)

        addQuery = "INSERT INTO Stock (productID, branchNo, stock) VALUES (%s, %s, %s)"

        exist = valueExists(self.branchExistQuery, (inputs[1],))
        exist += valueExists(self.productExistQuery, (inputs[0],))

        #Validation to ensure only existing values are entered
        if exist > 0:

            insertAndDeleteDB(addQuery, inputs)
            self.updateTable(self.stockQuery)
        
        else:
            messagebox.showwarning(title="Error", message="Invalid Branch No or Product Id")

    #Deletes data from database
    def deleteValues(self):
        
        deleteValue = self.stockId.getValue()

        if deleteValue != "":

            deleteValue = (deleteValue,)
            deleteQuery = "Delete FROM Stock where stockId=%s"
            insertAndDeleteDB(deleteQuery, deleteValue)
            self.updateTable(self.stockQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid Stock ID for Deletion")

class sales(tinker.Frame):
    
    def __init__(self, master):
        
        tinker.Frame.__init__(self, master)

        #Table Column Headings
        self.columnHeading = ["Sales Id", "Product Id", "Product Name", "Price", "Branch No", "Branch Name", "Customer Id", "Customer Name", "Amount", "Total", "Date Of Sale"]

        self.searchWraper = tinker.LabelFrame(self,  text="Search")
        self.dataWraper = tinker.LabelFrame(self,  text="Form") 
        self.tableWraper = tinker.LabelFrame(self, text="Sales Table")
 
        self.tableWraper.pack(fill="both", expand="yes", padx=20)
        self.salesQuery = "SELECT sl.salesId, pd.productId, pd.name, pd.price, br.branchNo, br.branchName, cs.customerID, Concat(cs.firstName, ' ', cs.lastName) as Full_Name, sl.amount, sl.total, sl.dateOfSale FROM Sales as sl JOIN Products as pd ON sl.productId=pd.productId JOIN Branch as br ON sl.branchNo=br.branchNo JOIN Customers as cs ON sl.customerID=cs.CustomerID"
        #Creating the Table
        self.salesTable = tableView(self.columnHeading, self.salesQuery, self.tableWraper)
        self.salesTable.getTable().bind("<Double 1>", self.getRowValue)

        self.productExistQuery = "SELECT EXISTS(SELECT * FROM Products WHERE productId=%s)"
        self.branchExistQuery = "SELECT EXISTS(SELECT * FROM Branch WHERE branchNo=%s)"
        self.customerExistQuery = "SELECT EXISTS(SELECT * FROM Customers WHERE customerID=%s)"

        #Search Warper
        self.searchWraper.pack(fill="both", expand="yes", padx=20)
        self.searchBlock = labelEntryView(self.searchWraper, 0, 0, "Sales Id:")
        self.branchBlock = labelEntryView(self.searchWraper, 0, 3, "Branch Id:")
        self.productBlock = labelEntryView(self.searchWraper, 1, 0, "Product Id:")

        self.searchButton = tinker.Button(self.searchWraper, command=self.searchId , text="Search")
        self.searchButton.grid(row=0, column=2)

        self.branchButton = tinker.Button(self.searchWraper, command=self.searchBranch , text="Search")
        self.branchButton.grid(row=0, column=5)

        self.productButton = tinker.Button(self.searchWraper, command=self.searchProduct , text="Search")
        self.productButton.grid(row=1, column=2)

        self.resetButton = tinker.Button(self.searchWraper, command=self.resetTable , text="Reset")
        self.resetButton.grid(row=2, column=2)

        self.blockList = [self.searchBlock, self.branchBlock, self.productBlock]

        #Data Wrapper
        self.dataWraper.pack(fill="both", expand="yes", padx=20)
        self.salesId = doubleLabelView(self.dataWraper, 0, 0, "Customer Id:")
        self.productId = labelEntryView(self.dataWraper, 1, 0, "Product Id:")
        self.productName = doubleLabelView(self.dataWraper, 2, 0, "Product Name:")
        self.productPrice = doubleLabelView(self.dataWraper, 3, 0, "Price:")
        self.amount = labelEntryView(self.dataWraper, 4, 0, "Amount:")
        self.total = doubleLabelView(self.dataWraper, 5, 0, "Total:")
        self.branchNo = labelEntryView(self.dataWraper, 0, 3, "Branch Id:")
        self.branchName = doubleLabelView(self.dataWraper, 1, 3, "Branch Name:")
        self.customerId = labelEntryView(self.dataWraper, 2, 3, "Customer Id:")
        self.customerName = doubleLabelView(self.dataWraper, 3, 3, "Customer Name:")
        self.salesDate = doubleLabelView(self.dataWraper, 4, 3, "Date of Sale:")

        self.insertButton = tinker.Button(self.dataWraper, text="Insert", command=self.insertValues)
        self.insertButton.grid(row=6, column=0)
        
        self.deleteButton = tinker.Button(self.dataWraper, text="Delete", command=self.deleteValues)
        self.deleteButton.grid(row=6, column=1)

        self.clearButton = tinker.Button(self.dataWraper, text="Clear Selected Data", command=self.clearValues)
        self.clearButton.grid(row=6, column=2)

        self.checkBranchbutton = tinker.Button(self.dataWraper, text="Check", command=self.checkBranch)
        self.checkBranchbutton.grid(row=0, column=5)

        self.checkCustomerbutton = tinker.Button(self.dataWraper, text="Check", command=self.checkCustomer)
        self.checkCustomerbutton.grid(row=2, column=5)

        self.checkProductbutton = tinker.Button(self.dataWraper, text="Check", command=self.checkProduct)
        self.checkProductbutton.grid(row=1, column=2)

        self.listLabel = [self.salesId, self.productName, self.productPrice, self.branchName, self.customerName, self.total, self.salesDate]
        self.listEntries = [self.productId, self.branchNo, self.customerId, self.amount]

        self.mainMenu = tinker.Button(self, text="Main Menu", command=lambda: self.master.switchFrame(mainMenu))
        self.mainMenu.pack()

    #Clear all values in entries and labels
    def clearValues(self):

        for o in self.blockList:
            o.deleteEntryValue(0)

        for i in self.listLabel:
            i.changeValue("")

        for j in self.listEntries:
            j.deleteEntryValue(0)

    #Updates the table
    def updateTable(self, query):

        self.clearValues()

        newData = noValueQuery(query)

        self.salesTable.changeTable(newData)

    #Resets the table
    def resetTable(self):

        self.updateTable(self.salesQuery)
        self.searchBlock.deleteEntryValue(0)

    #Search the table based on sales id
    def searchId(self):

        value = self.searchBlock.getEntryValue()

        if value != "" and value.isdecimal():

            idQuery = self.salesQuery + " WHERE salesId=%s"
            value = int(value)
            newData = valueQuery(idQuery, (value,))
            self.salesTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Sales Id for search")

    #Search the table based on branch No
    def searchBranch(self):

        value = self.branchBlock.getEntryValue()

        if value != "" and value.isdecimal():

            idQuery = self.salesQuery + " WHERE br.branchNo=%s"
            value = int(value)
            newData = valueQuery(idQuery, (value,))
            self.salesTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Branch No for search")

    #Search the table based on product Id
    def searchProduct(self):

        value = self.productBlock.getEntryValue()

        if value != "" and value.isdecimal():

            idQuery = self.salesQuery + " WHERE pd.productId=%s"
            value = int(value)
            newData = valueQuery(idQuery, (value,))
            self.salesTable.changeTable(newData)

        else:
            messagebox.showwarning(title="Error", message="Invalid Product Id for search")

    #Inserts table values into respected entires and labels
    def getRowValue(self, event):

        table = self.salesTable.getTable()
        
        rowId = table.identify_row(event.y)
        rowItems = table.item(table.focus())

        entriesValue = [1, 4, 6, 8]
        listValues = [0, 2, 3, 5, 7, 9, 10]

        for i, o in enumerate(self.listLabel):
            o.changeValue(rowItems["values"][listValues[i]])

        for i, o in enumerate(self.listEntries):
            o.entryRowValue(0, rowItems["values"][entriesValue[i]])

    #Checks if a branch exists
    def checkBranch(self):
        
        value = self.branchNo.getEntryValue()

        if value != "":

            exist = valueExists(self.branchExistQuery, (int(value),))

            if exist > 0:

                searchQuery = "SELECT branchName FROM Branch WHERE branchNo=%s"
                branchName = valueExists(searchQuery, (value,))
                self.branchName.changeValue(branchName)

            else:
                self.branchName.changeValue("null")

    #Checks if a product Exists
    def checkProduct(self):

        value =self.productId.getEntryValue()

        if value != "":

            exist = valueExists(self.productExistQuery, (int(value),))

            if exist > 0:

                searchQuery = "SELECT name, price FROM Products WHERE productId=%s"
                productData = valueQuery(searchQuery, (value,))
                self.productName.changeValue(productData[0][0])
                self.productPrice.changeValue(productData[0][1])

            else:
                self.productName.changeValue("null")
                self.productPrice.changeValue("null")

    #Checks if a customer Exists
    def checkCustomer(self):

        value =self.customerId.getEntryValue()

        if value != "":

            exist = valueExists(self.customerExistQuery, (int(value),))

            if exist > 0:

                searchQuery = "SELECT CONCAT(firstName, ' ', lastName) FROM Customers WHERE customerID=%s"
                customerName = valueExists(searchQuery, (value,))
                self.customerName.changeValue(customerName)

            else:
                self.customerName.changeValue("null")

    #Insert into database
    def insertValues(self):
        
        inputs = tuple()

        for i in self.listEntries:
            inputs += (i.getEntryValue(),)

        addQuery = "INSERT INTO Sales (productId, branchNo, customerId, amount, total, dateOfSale) VALUES (%s, %s, %s, %s, %s, %s)"

        exist = valueExists(self.productExistQuery, (inputs[0],))
        exist += valueExists(self.branchExistQuery, (inputs[1],))
        exist += valueExists(self.customerExistQuery, (inputs[2],))

        #Validates that only existing values are inserted
        if exist > 0:
            
            priceQuery = "SELECT price FROM Products WHERE productId=%s"

            priceOfProduct = valueExists(priceQuery, (inputs[0],))
            total = round(float(priceOfProduct) * float(inputs[3]), 2)
            dateNow = date.today()

            inputs += (total, dateNow)

            insertAndDeleteDB(addQuery, inputs)
            self.updateTable(self.salesQuery)
        
        else:
            messagebox.showwarning(title="Error", message="Invalid Values Entered, \nPlease use Check Button to see Invalid Values labelled Null")

    #Delete Rows From database
    def deleteValues(self):

        deleteValue = self.salesId.getValue()

        if deleteValue != "":

            deleteValue = (deleteValue,)
            deleteQuery = "Delete FROM Sales where salesId=%s"
            insertAndDeleteDB(deleteQuery, deleteValue)
            self.updateTable(self.salesQuery)

        else:
            messagebox.showwarning(title="Error", message="Invalid Sales ID for Deletion")