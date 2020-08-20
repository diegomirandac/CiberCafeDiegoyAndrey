from tkinter import StringVar #Para asociar los campos de texto con el compomente texto
from tkinter import IntVar #Para asociar los campos de numero con el compomente radio

class Proveedor: #POJO

    def __init__(self):
        self.Cedula = StringVar()
        self.telefono = StringVar()
        self.descripcion = StringVar()
        self.lastUser = ""
        self.lastModification = StringVar()

    def limpiar(self):
        self.Cedula.set("")
        self.telefono.set("")
        self.descripcion.set("")

    def printInfo(self):
        print(f"Cedula:{self.Cedula.get()}")
        print(f"Articulo:{self.PK_ID_ARTICULOS.get()}")
        print(f"Descripcion:{self.descripcion.get()}")

    
        