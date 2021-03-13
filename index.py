import pymongo
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIME = 1000

MONGO_URI = 'mongodb://' + MONGO_HOST+':'+MONGO_PORT+'/'

MONGO_BASEDATA = 'escuela'
MONGO_COLLECTION = 'alumnos'

client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME)
base_data = client[MONGO_BASEDATA]
collection = base_data[MONGO_COLLECTION]

def showData():
    try:
        registros=table.get_children()
        for registro in registros:
            table.delete(registro)
        for document in collection.find():
            table.insert('',0,text=document['_id'], values = document['nombre'])
            #print(document['nombre'] + " " + str(document['calificacion']))
        client.server_info()
        print('Connection successful')
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTime:
        print('Time lose: ' + errorTime)
    except pymongo.errors.ConnectionFailure as errorConnection:
        print('Connection: ' + errorConnection)

def create():
    if len(name.get())!=0 and len(classification.get())!=0 and len(sex.get())!=0 :
        try:
            document={"nombre":name.get(),"sexo":sex.get(),"clasificacion":classification.get()}
            collection.insert(document)
            name.delete(0,END)
            sex.delete(0,END)
            classification.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
        showData()

window = Tk()
table = ttk.Treeview(window, columns = 2)
table.grid(row = 1, column = 0, columnspan = 2)
table.heading("#0", text="ID")
table.heading("#1", text="Name")

# Name
Label(window, text="Name").grid(row=2,column=0)
name=Entry(window)
name.grid(row=2, column=1)

Label(window, text="Sex").grid(row=3,column=0)
sex=Entry(window)
sex.grid(row=3, column=1)


Label(window, text="Classification").grid(row=4,column=0)
classification=Entry(window)
classification.grid(row=4, column=1)

# Botton
crear=Button(window, text="Create student", command=create,bg="green",fg="white")
crear.grid(row=5,columnspan=2)
showData()
window.mainloop()
