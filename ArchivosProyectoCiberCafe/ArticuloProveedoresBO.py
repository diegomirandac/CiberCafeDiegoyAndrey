import mysql.connector # para instalarlo -> pip3 install mysql-connector 



class ArticuloProveedoresBO:

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
    def guardar(self, ArticuloProveedores):
        try:
            if(self.validar(ArticuloProveedores)):#se valida que tenga la información

                if(not self.exist(ArticuloProveedores)): #si no existe lo agrega
                    ArticuloProveedores.lastUser = "Diego"
                    
                    insertSQL = "INSERT INTO ArticuloProveedoress (`PK_ArticuloProveedores`, `PK_FK_cedula`, `descripcion`, `lastUser`, `lastModification`) VALUES (%s, %s, %s, %s, CURDATE())"
                    insertValores =  (ArticuloProveedores.ArticuloProveedores.get(),ArticuloProveedores.cedula.get(),ArticuloProveedores.descripcion.get(), ArticuloProveedores.lastUser)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El ArticuloProveedores indicado en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #*************************************************************************
    #Metodo que verifica en la base de datos si la persona existe por cédula
    #*************************************************************************
    def exist(self , ArticuloProveedores):
        try:
            existe = False
            selectSQL = "Select * from Proveedors where pk_ArticuloProveedores = " + ArticuloProveedores.ArticuloProveedores.get()
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
    def validar (self, ArticuloProveedores):
        valido = True
        ArticuloProveedores.printInfo()
        if ArticuloProveedores.cedula.get() == "" :
            valido = False
        
        if ArticuloProveedores.ArticuloProveedores.get() == "" :
            valido = False

        if ArticuloProveedores.descripcion.get() == "" :
            valido = False

        return valido

    #*************************************************************************
    #Metodo para consultar toda la información de la base de datos
    #*************************************************************************
    def consultar(self ):
        try:
            selectSQL = 'select t.PK_FK_cedula as cedula, \
                            CONCAT( p.nombre, " ", p.apellido1, " ", p.apellido2 ) as nombre, \
                            t.pk_ArticuloProveedores as ArticuloProveedores, \
                            t.descripcion \
                        from ArticuloProveedoress t inner join personas p on t.PK_FK_cedula = p.pk_cedula'
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
    def consultarProveedor(self, ArticuloProveedores):
        try:
            selectSQL = "Select * from ArticuloProveedoress where PK_ArticuloProveedores = " + ArticuloProveedores.ArticuloProveedores.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : #Metodo obtiene un solo registro o none si no existe información
                ArticuloProveedores.ArticuloProveedores.set(personaDB[0])
                ArticuloProveedores.cedula.set(personaDB[1])
                ArticuloProveedores.descripcion.set(personaDB[2])
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
    def eliminar(self, ArticuloProveedores):
        try:
            deleteSQL = "delete  from ArticuloProveedoress where PK_ArticuloProveedores = " + ArticuloProveedores.ArticuloProveedores.get()
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
    def modificar(self, ArticuloProveedores):
        try:
            if(self.validar(ArticuloProveedores)):#se valida que tenga la información

                if(self.exist(ArticuloProveedores)): #si  existe lo modifica
                    ArticuloProveedores.lastUser = "ChGari"
                    updateSQL = "UPDATE ArticuloProveedoress  set `PK_FK_cedula` = %s, `descripcion` = %s, `lastUser` = %s, `lastModification` = CURDATE() WHERE `PK_ArticuloProveedores` =  %s"
                    updateValores =  (ArticuloProveedores.cedula.get(),ArticuloProveedores.descripcion.get(),ArticuloProveedores.lastUser, ArticuloProveedores.ArticuloProveedores.get())
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
    


        
        