import mysql.connector 


class ProyectoBO:
    def __init__(self):
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "root", 
                                     db ="mydb") 

   
    def __del__(self):
        self.db.close() 
    def guardar(self, persona):
        try:
            if(self.validar(persona)):

                if(not self.exist(persona)):
                    persona.lastUser = "ChGari"
                    
                    insertSQL = "INSERT INTO Personas (`PK_cedula`, `nombre`, `apellido1`, `apellido2`, `fecNacimiento`, `sexo`, `comentario`, `tiempousuario`, `ultimousuario`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
                    insertValores =  (persona.cedula.get(),persona.nombre.get(),persona.apellido1.get(), persona.apellido2.get(), persona.fecNacimiento.get(), persona.sexo.get(), persona.observaciones.get(), persona.lastUser)
                    cursor = self.db.cursor()
                    cursor.execute(insertSQL, insertValores) 
                    self.db.commit() 
                else:
                    raise Exception('La cédula indicada en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    
    def exist(self , persona):
        try:
            existe = False
            selectSQL = "Select * from Personas where PK_cedula = " + persona.cedula.get()
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


    
    def validar (self, persona):
        valido = True
        persona.printInfo()
        if persona.cedula.get() == "" :
            valido = False
        
        if persona.nombre.get() == "" :
            valido = False

        if persona.apellido1.get() == "" :
            valido = False

        if persona.apellido2.get() == "" :
            valido = False

        if persona.fecNacimiento.get() == "" :
            valido = False
        
        if persona.sexo.get() == "" :
            valido = False
        
        if persona.comentario.get() == "" :
            valido = False

        return valido

   
    def consultar(self ):
        try:
            selectSQL = "select pk_cedula as cedula, \
                            nombre, apellido1, apellido2, \
                            fecNacimiento,  \
                            CASE sexo \
                                when 1 then 'Masculino' \
                                else        'Femenino' \
                            END AS sexo \
                        from personas" 
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


    def consultarPersona(self, persona):
        try:
            selectSQL = "Select * from Personas where PK_cedula = " + persona.cedula.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : 
                persona.cedula.set(personaDB[0])
                persona.nombre.set(personaDB[1])
                persona.apellido1.set(personaDB[2])
                persona.apellido2.set(personaDB[3])
                persona.fecNacimiento.set(personaDB[4])
                persona.sexo.set(personaDB[5])
                persona.observaciones.set(personaDB[6])
            else:
                raise Exception("La cédula consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

   
    def eliminar(self, persona):
        try:
            deleteSQL = "delete  from Personas where PK_cedula = " + persona.cedula.get()
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



    
    def modificar(self, persona):
        try:
            if(self.validar(persona)):

                if(self.exist(persona)):
                    persona.lastUser = "ChGari"
                    updateSQL = "UPDATE Personas  set `nombre` = %s, `apellido1` = %s, `apellido2` = %s, `fecNacimiento` = %s, `sexo` = %s, `comentario` = %s, `tiempousado` = %s, `ultimousuario` = CURDATE() WHERE `PK_cedula` =  %s"
                    updateValores =  (persona.nombre.get(),persona.apellido1.get(), persona.apellido2.get(), persona.fecNacimiento.get(), persona.sexo.get(), persona.observaciones.get(), persona.lastUser, persona.cedula.get())
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
    
        
