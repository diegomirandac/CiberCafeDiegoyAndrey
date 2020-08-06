from tkinter import StringVar 
from tkinter import IntVar 

class Telefono: 

    def __init__(self):
        self.cedula = StringVar()
        self.telefono = StringVar()
        self.descripcion = StringVar()
        self.lastUser = ""
        self.lastModification = StringVar()

    def limpiar(self):
        self.cedula.set("")
        self.telefono.set("")
        self.descripcion.set("")

    def printInfo(self):
        print(f"Cedula:{self.cedula.get()}")
        print(f"Telefono:{self.telefono.get()}")
        print(f"Descripcion:{self.descripcion.get()}")

    
        