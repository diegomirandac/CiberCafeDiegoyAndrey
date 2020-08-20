from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk 

from tksheet import Sheet # para instalarlo -> pip3 install tksheet

from tkcalendar import Calendar, DateEntry # para instalarlo -> pip3 install tkcalendar

#Incluye el objeto de cliente
from modelo import Cliente

#Incluye el objeto de logica de negocio
from modelo import ClientoBO

#incluye las otras pantallas
import mant_articulos
import mant_proveedores
import mant_ArticulosProveedores

#include para reportes, para instalar reportlab -> pip3 install reportlab
from reportlab.pdfgen import canvas as reportPDF
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors

#Importa para ejecutar un comando
import subprocess


class Aplicacion:
    

    def __init__(self):
        #*************************************************************************
        #Crea un objeto TK
        #*************************************************************************
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Clientes")
        self.raiz.geometry('900x600') 

        #*************************************************************************
        #crea el menu de la pantalla
        #*************************************************************************
        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Acerca de..")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="proveedor", command=self.mostrar_mant_proveedores)
        mantmenu.add_command(label="Articulos", command=self.mostrar_mant_articulos)
        mantmenu.add_command(label="Articulos del proveedor", command=self.mostrar_mant_ArticulosProveedores)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #*************************************************************************
        #crea un objeto tipo fuenta
        #*************************************************************************
        self.fuente = font.Font(weight="bold")

        #*************************************************************************
        #se crean atributos de la clase
        #*************************************************************************
        self.cliente = Cliente.Cliente() #se crea el objeto de dominio para guardar la información
        self.insertando = True
        
        #*************************************************************************
        #se crean los campos de la pantalla
        #*************************************************************************

        #Se coloca un label del titulo
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE CLIENTES", font = self.fuente)
        self.lb_tituloPantalla.place(x = 320, y = 20) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y
        
        #coloca en el formulario el campo y el label de cedula
        self.lb_Cedula = Label(self.raiz, text = "Cedula:")
        self.lb_Cedula.place(x = 240, y = 60)
        self.txt_Cedula = Entry(self.raiz, textvariable=self.cliente.Cedula, justify="right")
        self.txt_Cedula.place(x = 370, y = 60)

        #coloca en el formulario el campo y el label de nombre
        self.lb_nombre = Label(self.raiz, text = "Nombre:")
        self.lb_nombre.place(x = 240, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.cliente.nombre, justify="right", width=30)
        self.txt_nombre.place(x = 370, y = 90)

        #coloca en el formulario el campo y el label de apellido1
        self.lb_apellido1 = Label(self.raiz, text = "Primer apellido:")
        self.lb_apellido1.place(x = 240, y = 120)
        self.txt_apellido1 = Entry(self.raiz, textvariable=self.cliente.apellido1, justify="right", width=30)
        self.txt_apellido1.place(x = 370, y = 120)


        #coloca en el formulario el campo y el label de apellido2
        self.lb_apellido2 = Label(self.raiz, text = "Segundo apellido:")
        self.lb_apellido2.place(x = 240, y = 150)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.cliente.apellido2, justify="right", width=30)
        self.txt_apellido2.place(x = 370, y = 150)

        #coloca en el formulario el campo y el label de fecha nacimiento
        self.lb_Fecha_Nacimiento = Label(self.raiz, text = "Fecha nacimiento:")
        self.lb_Fecha_Nacimiento.place(x = 240, y = 180)
        self.txt_FechaNacimiento = Entry(self.raiz, textvariable=self.cliente.FechaNacimiento, justify="right", width=30, state="readonly")
        self.txt_FechaNacimiento.place(x = 370, y = 180)
        self.bt_mostrarCalendario = Button(self.raiz, text="...", width=3, command = self.mostrarDatePicker)
        self.bt_mostrarCalendario.place(x = 650, y = 180)

        #coloca en el formulario el campo y el label de sexo
        self.lb_sexo = Label(self.raiz, text = "Sexo:")
        self.lb_sexo.place(x = 240, y = 210)
        self.radio_sexoM = Radiobutton(self.raiz, text="Masculino", variable=self.cliente.sexo,   value=1)
        self.radio_sexoF = Radiobutton(self.raiz, text="Femenino", variable=self.cliente.sexo,   value=2)
        self.radio_sexoM.place(x = 370, y = 210)
        self.radio_sexoF.place(x = 490, y = 210)
        self.cliente.sexo.set(1) #setea el sexo al inicio como masculino

        #coloca en el formulario el campo y el label de observaciones
        self.lb_observaciones = Label(self.raiz, text = "Observaciones:")
        self.lb_observaciones.place(x = 240, y = 250)
        self.txt_observaciones = Entry(self.raiz, textvariable=self.cliente.observaciones, justify="right", width=30)
        self.txt_observaciones.place(x = 370, y = 250)

        #coloca los botones enviar y borrar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.limpiarInformacion)
        self.bt_borrar.place(x = 370, y = 310)

        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command = self.enviarInformacion)
        self.bt_enviar.place(x = 510, y = 310)

        self.bt_modificar = Button(self.raiz, text="Modificar", width=15, command = self.enviarInformacion)
        self.bt_modificar.place(x = 650, y = 310)

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 350, y = 355) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y

        #*************************************************************************
        #tabla con informacion
        #*************************************************************************
        
        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['Cédula', 'Nombre', 'Primer Ape.', 'Segundo Ape.', 'FechaNacimiento', 'Sexo'],
                            height = 195, #height and width arguments are optional
                            width = 720 #For full startup arguments see DOCUMENTATION.md
                            )
        
        self.sheet.enable_bindings(("single_select", 
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    #"row_width_resize",
                                    #"column_height_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_column",
                                    "rc_delete_column",
                                    "rc_insert_row",
                                    "rc_delete_row"))
        self.sheet.place(x = 20, y = 390)

        #*************************************************************************
        #coloca los botones cargar y eliminar
        #*************************************************************************
        self.bt_cargar = Button(self.raiz, text="Cargar", width=15, command = self.cargarInformacion)
        self.bt_cargar.place(x = 750, y = 385)

        self.bt_eliminar = Button(self.raiz, text="Eliminar", width=15, command = self.eliminarInformacion)
        self.bt_eliminar.place(x = 750, y = 425)

        self.bt_reporte = Button(self.raiz, text="Reporte", width=15, command = self.generarPDFListado)
        self.bt_reporte.place(x = 750, y = 465)
        
        #*************************************************************************
        #se llama el metodo para cargar la informacion
        #*************************************************************************
        self.cargarTodaInformacion()


        #*************************************************************************
        #se inicial el main loop de la pantalla
        #*************************************************************************
        self.raiz.mainloop()

    #*************************************************************************
    #Llamadas a otras pantallas
    #*************************************************************************
    def generarPDFListado(self):
        try:
            #Crea un objeto para la creación del PDF
            nombreArchivo = "ListadoClientes.pdf"
            rep = reportPDF.Canvas(nombreArchivo)

            #Agrega el tipo de fuente Arial
            registerFont(TTFont('Arial','ARIAL.ttf'))
            
        
            #Crea el texto en donde se incluye la información
            textobject = rep.beginText()
            # Coloca el titulo
            textobject.setFont('Arial', 16)
            textobject.setTextOrigin(10, 800)
            textobject.setFillColor(colors.darkorange)
            textobject.textLine(text='LISTA DE CLIENTES')
            #Escribe el titulo en el reportes
            rep.drawText(textobject)

            #consultar la informacion de la base de datos
            self.clienteBo = ClientoBO.ClienteBO() #se crea un objeto de logica de negocio
            informacion = self.clienteBo.consultar()
            #agrega los titulos de la tabla en la información consultada
            titulos = ["Cédula","Nombre","Primer Apellido","Segundo apellido","FechaNacimiento", "Sexo"]
            informacion.insert(0,titulos)
            #crea el objeto tabla  para mostrar la información
            t = Table(informacion)
            #Le coloca el color tanto al borde de la tabla como de las celdas
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                  ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

            #para cambiar el color de las fichas de hace un ciclo según la cantidad de datos
            #que devuelve la base de datos
            data_len = len(informacion)
            for each in range(data_len):
                if each % 2 == 0:
                    bg_color = colors.whitesmoke
                else:
                    bg_color = colors.lightgrey

                if each == 0 : #Le aplica un estilo diferente a la tabla
                    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), colors.orange)]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

            #acomoda la tabla según el espacio requerido
            aW = 840
            aH = 780
            w, h = t.wrap(aW, aH)
            t.drawOn(rep, 10, aH-h)

            #Guarda el archivo
            rep.save()
            #Abre el archivo desde comandos, puede variar en MacOs es open
            #subprocess.Popen("open '%s'" % nombreArchivo, shell=True)
            subprocess.Popen(nombreArchivo, shell=True) #Windows
        except IOError:
            msg.showerror("Error",  "El archivo ya se encuentra abierto") 

    #*************************************************************************
    #Llamadas a otras pantallas
    #*************************************************************************
    def mostrar_mant_articulos(self):
       mant_articulos.MantArticulos(self.raiz)

    def mostrar_mant_proveedores(self):
       mant_proveedores.MantProveedores(self.raiz)

    def mostrar_mant_ArticulosProveedores(self):
        mant_ArticulosProveedores.MantArticulosProveedores(self.raiz)

    #*************************************************************************
    #Metodo para consultar la información de la base de datos para 
    #cargarla en la tabla
    #*************************************************************************
    def cargarTodaInformacion(self):
        try:
            self.clienteBo = ClientoBO.ClienteBO() #se crea un objeto de logica de negocio
            resultado = self.clienteBo.consultar()

            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para cargar informacion
    #*************************************************************************
    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            cedula = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            self.cliente.Cedula.set(cedula)
            self.clienteBo = ClientoBO.ClienteBO() #se crea un objeto de logica de negocio
            self.clienteBo.consultarCliente(self.cliente) #se envia a consultar
            self.insertando = False
            msg.showinfo("Acción: Consultar cliente", "La información de la cliente ha sido consultada correctamente") # Se muestra el mensaje de que todo esta correcto
            
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para cargar eliminar la informacion
    #*************************************************************************
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            Cedula = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar a "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.cliente.Cedula.set(Cedula)
                self.clienteBo = ClientoBO.ClienteBO() #se crea un objeto de logica de negocio
                self.clienteBo.eliminar(self.cliente) #se envia a consultar
                self.cargarTodaInformacion()
                self.cliente.limpiar()
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    
    def printTxt(self, texto):
        print(texto)


    #*************************************************************************
    #Metodo para enviar la información a la base de datos
    #*************************************************************************
    def enviarInformacion(self):
        try:
            self.clienteBo = ClientoBO.ClienteBO() #se crea un objeto de logica de negocio
            if(self.insertando == True):
                self.clienteBo.guardar(self.cliente)
            else:
                self.clienteBo.modificar(self.cliente)
            
            self.cargarTodaInformacion()
            self.cliente.limpiar() #se limpia el formulario

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar cliente", "La información de la cliente ha sido incluida correctamente") # Se muestra el mensaje de que todo esta correcto
            else:
                msg.showinfo("Acción: Agregar modificar", "La información de la cliente ha sido modificada correctamente") # Se muestra el mensaje de que todo esta correcto
            
            self.insertando = True

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para limpiar el formulario
    #*************************************************************************
    def limpiarInformacion(self):
        self.cliente.limpiar() #llama al metodo de la clase cliente para limpiar los atritudos de la clase
        self.insertando = True
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente") # muestra un mensaje indicando que se limpio el formulario


    #*************************************************************************
    #Metodo para mostrar un contro tipo datepicker
    #*************************************************************************
    def mostrarDatePicker(self):
        self.top = Toplevel(self.raiz)
        self.cal = Calendar(self.top, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand", year=2019, month=6, day=16)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="Seleccionar", command = self.seleccionarFecha).pack()

    #*************************************************************************
    #Evento para obtener la fecha del datepicker
    #*************************************************************************
    def seleccionarFecha(self):
        self.cliente.FechaNacimiento.set(self.cal.selection_get())

    

def main():
    Aplicacion()
    return 0

if __name__ == "__main__":
    main()