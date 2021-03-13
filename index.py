from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIME = 1000

MONGO_URI = 'mongodb://' + MONGO_HOST+':'+MONGO_PORT+'/'

MONGO_BASEDATA = 'escuela'
MONGO_COLLECTION = 'alumnos'

client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME)
base_data = client[MONGO_BASEDATA]
collection = base_data[MONGO_COLLECTION]
ID_ALUMNO = ""
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
    if len(name.get())!=0 and len(score.get())!=0 and len(sex.get())!=0 :
        try:
            document={"nombre":name.get(),"sexo":sex.get(),"score":score.get()}
            collection.insert(document)
            name.delete(0,END)
            sex.delete(0,END)
            score.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
        showData()

# SEARCH
def doubleClickTable(event):
    global ID_ALUMNO
    ID_ALUMNO = str(table.item(table.selection())["text"])
    #print(ID_ALUMNO)
    document = collection.find({'_id' : ObjectId(ID_ALUMNO)})[0]
    #print(document)
    # Delete from the first for final
    name.delete(0, END)
    name.insert(0,document['nombre'])
    sex.delete(0, END)
    sex.insert(0,document['sexo'])
    score.delete(0, END)
    score.insert(0,document['score'])
    crear['state']='disabled'
    editar['state']='normal'

def editarR():
    global ID_ALUMNO
    if len(name.get())!=0 and len(score.get())!=0 and len(sex.get())!=0 :
        try:
            idSearch={"_id":ObjectId(ID_ALUMNO)}
            newValues = {"nombre":name.get(), "sexo":sex.get(), "score":score.get()}
            collection.update(idSearch,newValues)
            name.delete(0,END)
            sex.delete(0,END)
            score.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    showData()
    crear['state']='normal'
    editar['state']='disabled'

window = Tk()
table = ttk.Treeview(window, columns = 2)
table.grid(row = 1, column = 0, columnspan = 2)
table.heading("#0", text="ID")
table.heading("#1", text="Name")
table.bind("<Double-Button-1>", doubleClickTable)
# Name
Label(window, text="Name").grid(row=2,column=0)
name=Entry(window)
name.grid(row=2, column=1)

Label(window, text="Sex").grid(row=3,column=0)
sex=Entry(window)
sex.grid(row=3, column=1)


Label(window, text="score").grid(row=4,column=0)
score=Entry(window)
score.grid(row=4, column=1)

# Botton
crear=Button(window, text="Create student", command=create,bg="green",fg="white")
crear.grid(row=5,columnspan=2)

# Edit

editar=Button(window, text="Edit student", command=editarR,bg="green",fg="yellow")
editar.grid(row=6,columnspan=2)
editar['state'] = 'disabled'
showData()
window.mainloop()
