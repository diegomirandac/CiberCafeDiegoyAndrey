import mysql.connector 



class TelefonoBO:

    
    def __init__(self):
        
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "root", 
                                     db ="mydb") 

    
    def __del__(self):
        self.db.close() 
  
    
    def guardar(self, telefono):
        try:
            if(self.validar(telefono)):

                if(not self.exist(telefono)): 
                    telefono.lastUser = "ChGari"
                    
                    insertSQL = "INSERT INTO telefonos (`PK_telefono`, `PK_FK_cedula`, `descripcion`, `lastUser`, `lastModification`) VALUES (%s, %s, %s, %s, CURDATE())"
                    insertValores =  (telefono.telefono.get(),telefono.cedula.get(),telefono.descripcion.get(), telefono.lastUser)
                    cursor = self.db.cursor() 
                    cursor.execute(insertSQL, insertValores) 
                    self.db.commit() 
                else:
                    raise Exception('El telefono indicado en el formulario existe en la base de datos')  
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
   
    def exist(self , telefono):
        try:
            existe = False
            selectSQL = "Select * from Telefonos where pk_telefono = " + telefono.telefono.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) : 
                existe  = True

            return existe
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 


    
    def validar (self, telefono):
        valido = True
        telefono.printInfo()
        if telefono.cedula.get() == "" :
            valido = False
        
        if telefono.telefono.get() == "" :
            valido = False

        if telefono.descripcion.get() == "" :
            valido = False

        return valido

    
    def consultar(self ):
        try:
            selectSQL = 'select t.PK_FK_cedula as cedula, \
                            CONCAT( p.nombre, " ", p.apellido1, " ", p.apellido2 ) as nombre, \
                            t.pk_telefono as telefono, \
                            t.descripcion \
                        from telefonos t inner join personas p on t.PK_FK_cedula = p.pk_cedula'
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


    
    def consultarTelefono(self, telefono):
        try:
            selectSQL = "Select * from telefonos where PK_telefono = " + telefono.telefono.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            clienteDB = cursor.fetchone()
            if (clienteDB) : 
                telefono.telefono.set(clienteDB[0])
                telefono.cedula.set(clienteDB[1])
                telefono.descripcion.set(clienteDB[2])
            else:
                raise Exception("La cédula consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    def eliminar(self, telefono):
        try:
            deleteSQL = "delete  from telefonos where PK_telefono = " + telefono.telefono.get()
            cursor = self.db.cursor() 
            cursor.execute(deleteSQL) 
            self.db.commit() 
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            if str(e) == "tiene FK":
                raise Exception("El dato no se puede eliminar por que tiene datos asociados, por favor eliminarlos primero")     
            else:
                raise Exception(str(e)) 



    
    def modificar(self, telefono):
        try:
            if(self.validar(telefono)):

                if(self.exist(telefono)): 
                    telefono.lastUser = "ChGari"
                    updateSQL = "UPDATE telefonos  set `PK_FK_cedula` = %s, `descripcion` = %s, `lastUser` = %s, `lastModification` = CURDATE() WHERE `PK_telefono` =  %s"
                    updateValores =  (telefono.cedula.get(),telefono.descripcion.get(),telefono.lastUser, telefono.telefono.get())
                   
                    cursor = self.db.cursor() 
                    cursor.execute(updateSQL, updateValores) 
                    self.db.commit() 
                else:
                    raise Exception('La cédula indicada en el formulario no existe en la base de datos')  
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    


        
        