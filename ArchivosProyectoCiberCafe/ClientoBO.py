import mysql.connector # para instalarlo -> pip3 install mysql-connector 



class ClienteBO:

    #*************************************************************************
    #El constructor de la clase cliente BO crea un objeto de conexion a la base de datos
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
    #Metodo que guarda una cliente en la base de datos
    #*************************************************************************
    def guardar(self, cliente):
        try:
            if(self.validar(cliente)):#se valida que tenga la información

                if(not self.exist(cliente)): #si no existe lo agrega
                    cliente.lastUser = "Diego"
                    
                    insertSQL = "INSERT INTO clientes (`PK_Cedula`, `nombre`, `apellido1`, `apellido2`, `FechaNacimiento`, `sexo`, `observaciones`, `lastUser`, `lastModification`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
                    insertValores =  (cliente.Cedula.get(),cliente.nombre.get(),cliente.apellido1.get(), cliente.apellido2.get(), cliente.FechaNacimiento.get(), cliente.sexo.get(), cliente.observaciones.get(), cliente.lastUser)
                    #print(insertValores)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('La cédula indicada en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #*************************************************************************
    #Metodo que verifica en la base de datos si la cliente existe por cédula
    #*************************************************************************
    def exist(self , cliente):
        try:
            existe = False
            selectSQL = "Select * from clientes where PK_Cedula = " + cliente.Cedula.get()
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
    def validar (self, cliente):
        valido = True
        cliente.printInfo()
        if cliente.Cedula.get() == "" :
            valido = False
        
        if cliente.nombre.get() == "" :
            valido = False

        if cliente.apellido1.get() == "" :
            valido = False

        if cliente.apellido2.get() == "" :
            valido = False

        if cliente.FechaNacimiento.get() == "" :
            valido = False
        
        if cliente.sexo.get() == "" :
            valido = False
        
        if cliente.observaciones.get() == "" :
            valido = False

        return valido

    #*************************************************************************
    #Metodo para consultar toda la información de la base de datos
    #*************************************************************************
    def consultar(self ):
        try:
            selectSQL = "select pk_Cedula as Cedula, \
                            nombre, apellido1, apellido2, \
                            FechaNacimiento,  \
                            CASE sexo \
                                when 1 then 'Masculino' \
                                else        'Femenino' \
                            END AS sexo \
                        from clientes" 
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
    #Metodo para consultar la información de una cliente
    #*************************************************************************
    def consultarcliente(self, cliente):
        try:
            selectSQL = "Select * from clientes where PK_Cedula = " + cliente.Cedula.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            clienteDB = cursor.fetchone()
            if (clienteDB) : #Metodo obtiene un solo registro o none si no existe información
                cliente.cedula.set(clienteDB[0])
                cliente.nombre.set(clienteDB[1])
                cliente.apellido1.set(clienteDB[2])
                cliente.apellido2.set(clienteDB[3])
                cliente.FechaNacimiento.set(clienteDB[4])
                cliente.sexo.set(clienteDB[5])
                cliente.observaciones.set(clienteDB[6])
            else:
                raise Exception("La cédula consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #*************************************************************************
    #Metodo para eliminar a una cliente de la base de datos
    #*************************************************************************
    def eliminar(self, cliente):
        try:
            deleteSQL = "delete  from clientes where PK_Cedula = " + cliente.Cedula.get()
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
    #Metodo que guarda una cliente en la base de datos
    #*************************************************************************
    def modificar(self, cliente):
        try:
            if(self.validar(cliente)):#se valida que tenga la información

                if(self.exist(cliente)): #si  existe lo modifica
                    cliente.lastUser = "DiegoM"
                    updateSQL = "UPDATE clientes  set `nombre` = %s, `apellido1` = %s, `apellido2` = %s, `FechaNacimiento` = %s, `sexo` = %s, `observaciones` = %s, `lastUser` = %s, `lastModification` = CURDATE() WHERE `PK_Cedula` =  %s"
                    updateValores =  (cliente.nombre.get(),cliente.apellido1.get(), cliente.apellido2.get(), cliente.FechaNacimiento.get(), cliente.sexo.get(), cliente.observaciones.get(), cliente.lastUser, cliente.Cedula.get())
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
    


        
        