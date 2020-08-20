import mysql.connector # para instalarlo -> pip3 install mysql-connector 



class ProveedorBO:

    #*************************************************************************
    #El constructor de la clase persona BO crea un objeto de conexion a la base de datos
    #*************************************************************************
    def __init__(self):
        #se crea la conexión con la base de datos
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "letsrock@1993", 
                                     db ="mydb") 

    #*************************************************************************
    #Cuando el objeto es destruido por el interprete realiza la desconexion con la base de datos
    #*************************************************************************
    def __del__(self):
        self.db.close() #al destriurse el objeto cierra la conexion 
  
    #*************************************************************************
    #Metodo que guarda una persona en la base de datos
    #*************************************************************************
    def guardar(self, proveedor):
        try:
            if(self.validar(proveedor)):#se valida que tenga la información

                if(not self.exist(proveedor)): #si no existe lo agrega
                    proveedor.lastUser = "Diego"
                    
                    insertSQL = "INSERT INTO proveedors (`PK_proveedor`, `PK_FK_cedula`, `descripcion`, `lastUser`, `lastModification`) VALUES (%s, %s, %s, %s, CURDATE())"
                    insertValores =  (proveedor.proveedor.get(),proveedor.cedula.get(),proveedor.descripcion.get(), proveedor.lastUser)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El proveedor indicado en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #*************************************************************************
    #Metodo que verifica en la base de datos si la persona existe por cédula
    #*************************************************************************
    def exist(self , proveedor):
        try:
            existe = False
            selectSQL = "Select * from Proveedors where pk_proveedor = " + proveedor.proveedor.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) : #Metodo obtiene un solo registro o none si no existe información
                existe  = True

            return existe
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 


    #*************************************************************************
    #Metodo para validar al información que proviene de la vista
    #*************************************************************************
    def validar (self, proveedor):
        valido = True
        proveedor.printInfo()
        if proveedor.cedula.get() == "" :
            valido = False
        
        if proveedor.proveedor.get() == "" :
            valido = False

        if proveedor.descripcion.get() == "" :
            valido = False

        return valido

    #*************************************************************************
    #Metodo para consultar toda la información de la base de datos
    #*************************************************************************
    def consultar(self ):
        try:
            selectSQL = 'select t.PK_FK_cedula as cedula, \
                            CONCAT( p.nombre, " ", p.apellido1, " ", p.apellido2 ) as nombre, \
                            t.pk_proveedor as proveedor, \
                            t.descripcion \
                        from proveedors t inner join personas p on t.PK_FK_cedula = p.pk_cedula'
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            myresult = cursor.fetchall()
            final_result = [list(i) for i in myresult]
            return final_result
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 


    #*************************************************************************
    #Metodo para consultar la información de una persona
    #*************************************************************************
    def consultarProveedor(self, proveedor):
        try:
            selectSQL = "Select * from proveedors where PK_proveedor = " + proveedor.proveedor.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : #Metodo obtiene un solo registro o none si no existe información
                proveedor.proveedor.set(personaDB[0])
                proveedor.cedula.set(personaDB[1])
                proveedor.descripcion.set(personaDB[2])
            else:
                raise Exception("La cédula consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #*************************************************************************
    #Metodo para eliminar a una persona de la base de datos
    #*************************************************************************
    def eliminar(self, proveedor):
        try:
            deleteSQL = "delete  from proveedors where PK_proveedor = " + proveedor.proveedor.get()
            cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
            cursor.execute(deleteSQL) #ejecuta el SQL con las valores
            self.db.commit() #crea un commit en la base de datos
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            if str(e) == "tiene FK":
                raise Exception("El dato no se puede eliminar por que tiene datos asociados, por favor eliminarlos primero")     
            else:
                raise Exception(str(e)) 



    #*************************************************************************
    #Metodo que guarda una persona en la base de datos
    #*************************************************************************
    def modificar(self, proveedor):
        try:
            if(self.validar(proveedor)):#se valida que tenga la información

                if(self.exist(proveedor)): #si  existe lo modifica
                    proveedor.lastUser = "ChGari"
                    updateSQL = "UPDATE proveedors  set `PK_FK_cedula` = %s, `descripcion` = %s, `lastUser` = %s, `lastModification` = CURDATE() WHERE `PK_proveedor` =  %s"
                    updateValores =  (proveedor.cedula.get(),proveedor.descripcion.get(),proveedor.lastUser, proveedor.proveedor.get())
                    #print(insertValores)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(updateSQL, updateValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('La cédula indicada en el formulario no existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    


        
        