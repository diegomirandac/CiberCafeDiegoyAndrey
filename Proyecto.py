from tkinter import StringVar
from tkinter import IntVar 

class Proyecto: 

    def __init__(self):
        self.cedula = StringVar()
        self.nombre = StringVar()
        self.apellido1 = StringVar()
        self.apellido2 = StringVar()
        self.fecNacimiento = StringVar()
        self.sexo = IntVar()
        self.comentario = StringVar()
        self.tiempousado = ""
        self.ultimousuario = StringVar()

    def limpiar(self):
        self.cedula.set("")
        self.nombre.set("")
        self.apellido1.set("")
        self.apellido2.set("")
        self.fecNacimiento.set("")
        self.sexo.set(1)
        self.comentario.set("")

    def printInfo(self):
        print(f"Cedula:{self.cedula.get()}")
        print(f"Nombre:{self.nombre.get()}")
        print(f"Apellido1:{self.apellido1.get()}")
        print(f"Apellido2:{self.apellido2.get()}")
        print(f"Fecha Nacimiento:{self.fecNacimiento.get()}")
        print(f"Sexo:{self.sexo.get()}")
        print(f"Comentario:{self.comentario.get()}")
