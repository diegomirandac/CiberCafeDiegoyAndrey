from tkinter import StringVar #Para asociar los campos de texto con el compomente texto
from tkinter import IntVar #Para asociar los campos de numero con el compomente radio

class Cliente: #POJO

    def __init__(self):
        self.Cedula = StringVar()
        self.nombre = StringVar()
        self.apellido1 = StringVar()
        self.apellido2 = StringVar()
        self.FechaNacimiento = StringVar()
        self.sexo = IntVar()
        self.observaciones = StringVar()
        self.lastUser = ""
        self.lastModification = StringVar()

    def limpiar(self):
        self.Cedula.set("")
        self.nombre.set("")
        self.apellido1.set("")
        self.apellido2.set("")
        self.FechaNacimiento.set("")
        self.sexo.set(1)
        self.observaciones.set("")

    def printInfo(self):
        print(f"Cedula:{self.Cedula.get()}")
        print(f"Nombre:{self.nombre.get()}")
        print(f"Apellido1:{self.apellido1.get()}")
        print(f"Apellido2:{self.apellido2.get()}")
        print(f"Fecha Nacimiento:{self.FechaNacimiento.get()}")
        print(f"Sexo:{self.sexo.get()}")
        print(f"Observaciones:{self.observaciones.get()}")

    
        