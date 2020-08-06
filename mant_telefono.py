from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk 


from tksheet import Sheet 

from tkcalendar import Calendar, DateEntry 

from modelo import Telefono
from modelo import Cliente

from modelo import TelefonoBO
from modelo import ClienteBO

class MantTelefono():
    

    def __init__(self, parent):
        self.parent = parent

        self.raiz = Toplevel(self.parent) 
        self.raiz.title ("Mantenimiento de Telefonos")
        self.raiz.geometry('900x510') 

        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Acerca de..")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Personas", command=self.mostrar_mant_personas)
        mantmenu.add_command(label="Direcciones")

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        
        self.fuente = font.Font(weight="bold")

      
        self.telefono = Telefono.Telefono() 
        self.insertando = True
        self.nombreCliente = StringVar() 

        self.Cliente = Cliente.Cliente()
        
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE TELEFONOS", font = self.fuente)
        self.lb_tituloPantalla.place(x = 320, y = 20) 
        
        self.lb_cedula = Label(self.raiz, text = "Cedula:")
        self.lb_cedula.place(x = 240, y = 60)
        self.txt_cedula = Entry(self.raiz, textvariable=self.telefono.cedula, justify="right", width=12)
        self.txt_cedula.place(x = 370, y = 60)

        self.bt_consultar = Button(self.raiz, text="Consultar", width=15, command = self.consultarNombre)
        self.bt_consultar.place(x = 512, y = 60)

        self.lb_nombre = Label(self.raiz, text = "Nombre:")
        self.lb_nombre.place(x = 240, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.nombrePersona, justify="right", width=30)
        self.txt_nombre.place(x = 370, y = 90)

        self.lb_telefono = Label(self.raiz, text = "Telefono:")
        self.lb_telefono.place(x = 240, y = 120)
        self.txt_telefono = Entry(self.raiz, textvariable=self.telefono.telefono, justify="right", width=30)
        self.txt_telefono.place(x = 370, y = 120)

        self.lb_descripcion = Label(self.raiz, text = "Descripción:")
        self.lb_descripcion.place(x = 240, y = 150)
        self.txt_descripcion = Entry(self.raiz, textvariable=self.telefono.descripcion, justify="right", width=30)
        self.txt_descripcion.place(x = 370, y = 150)

        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command=self.limpiarInformacion)
        self.bt_borrar.place(x = 370, y = 180)

        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command=self.enviarInformacion)
        self.bt_enviar.place(x = 510, y = 180)

        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 350, y = 230) 
        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['Cédula', 'Nombre', 'Telefono', 'Descripción'],
                            height = 195, 
                            width = 720 
                            )
        
        self.sheet.enable_bindings(("single_select", 
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_column",
                                    "rc_delete_column",
                                    "rc_insert_row",
                                    "rc_delete_row"))
        self.sheet.place(x = 20, y = 260)

       
        self.bt_cargar = Button(self.raiz, text="Cargar", width=15, command=self.cargarInformacion)
        self.bt_cargar.place(x = 750, y = 255)

        self.bt_eliminar = Button(self.raiz, text="Eliminar", width=15, command=self.eliminarInformacion)
        self.bt_eliminar.place(x = 750, y = 295)
        
       
        self.cargarTodaInformacion()

        
        self.parent.withdraw()

       
        self.raiz.protocol("WM_DELETE_WINDOW", self.on_closing) 

    def enviarInformacion(self):
        try:
            self.telefonoBo = TelefonoBO.TelefonoBO() 
            if(self.insertando == True):
                self.telefonoBo.guardar(self.telefono)
            else:
                self.telefonoBo.modificar(self.telefono)
            
            self.cargarTodaInformacion()
            self.telefono.limpiar()
            self.nombreCliente.set("")

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar teléfono", "La información del teléfono ha sido incluida correctamente") 
            else:
                msg.showinfo("Acción: Modificar teléfono", "La información del teléfono ha sido modificada correctamente") 
            
            self.insertando = True

        except Exception as e: 
            msg.showerror("Error",  str(e)) 

   
    def limpiarInformacion(self):
        self.telefono.limpiar() 
        self.nombreCliente.set("")
        self.insertando = True
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente") 


    
    def consultarNombre(self):
        try:
            self.ClienteBo = PersonoBO.ClienteBO()
            self.Cliente.cedula.set(self.telefono.cedula.get()) 
            self.ClienteBo.consultarCliente(self.Cliente) 
            if self.Cliente.nombre.get() == "" :
                self.nombreCliente = "No existe el Cliente "
            else:
                self.nombreCliente.set(self.Cliente.nombre.get() + " " + self.Cliente.apellido1.get() + " " + self.Cliente.apellido2.get())

        except Exception as e: 
            msg.showerror("Error",  str(e)) 

   
    def cargarTodaInformacion(self):
        try:
            self.telefonoBo = TelefonoBO.TelefonoBO() 
            resultado = self.telefonoBo.consultar()

            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e)) 


    
    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            telefono = (self.sheet.get_cell_data(datoSeleccionado[0],2))
            self.telefono.telefono.set(telefono)
            self.telefonoBo = TelefonoBO.TelefonoBO() 
            self.telefonoBo.consultarTelefono(self.telefono) 
            self.consultarNombre()
            self.insertando = False
            msg.showinfo("Acción: Consultar teléfono", "La información del teléfono ha sido consultada correctamente") 
            
        except Exception as e: 
            msg.showerror("Error",  str(e)) 

    
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            telefono = (self.sheet.get_cell_data(datoSeleccionado[0],2))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar el telefono "+telefono+" de "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.telefono.telefono.set(telefono)
                self.telefonoBo = TelefonoBO.TelefonoBO() 
                self.telefonoBo.eliminar(self.telefono) 
                self.cargarTodaInformacion()
                self.telefono.limpiar()
                self.nombreCliente.set("")

        except Exception as e: 
            msg.showerror("Error",  str(e)) 

    
    def mostrar_mant_cliente(self):
        self.parent.deiconify()
        self.raiz.destroy()

    def on_closing(self):
       self.parent.destroy()

  

