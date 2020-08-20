import mysql.connector # para instalarlo -> pip3 install mysql-connector 



class ArticuloBO:

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
    def guardar(self, articulo):
        try:
            if(self.validar(articulo)):#se valida que tenga la información

                if(not self.exist(articulo)): #si no existe lo agrega
                    articulo.lastUser = "Diego"
                    
                    insertSQL = "INSERT INTO articulos (`PK_articulo`, `PK_FK_cedula`, `descripcion`, `lastUser`, `lastModification`) VALUES (%s, %s, %s, %s, CURDATE())"
                    insertValores =  (articulo.articulo.get(),articulo.cedula.get(),articulo.descripcion.get(), articulo.lastUser)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El articulo indicado en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #*************************************************************************
    #Metodo que verifica en la base de datos si la persona existe por cédula
    #*************************************************************************
    def exist(self , articulo):
        try:
            existe = False
            selectSQL = "Select * from Articulos where pk_articulo = " + articulo.articulo.get()
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
    def validar (self, articulo):
        valido = True
        articulo.printInfo()
        if articulo.cedula.get() == "" :
            valido = False
        
        if articulo.articulo.get() == "" :
            valido = False

        if articulo.descripcion.get() == "" :
            valido = False

        return valido

    #*************************************************************************
    #Metodo para consultar toda la información de la base de datos
    #*************************************************************************
    def consultar(self ):
        try:
            selectSQL = 'select t.PK_FK_cedula as cedula, \
                            CONCAT( p.nombre, " ", p.apellido1, " ", p.apellido2 ) as nombre, \
                            t.pk_articulo as articulo, \
                            t.descripcion \
                        from articulos t inner join personas p on t.PK_FK_cedula = p.pk_cedula'
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
    def consultarArticulo(self, articulo):
        try:
            selectSQL = "Select * from articulos where PK_articulo = " + articulo.articulo.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : #Metodo obtiene un solo registro o none si no existe información
                articulo.articulo.set(personaDB[0])
                articulo.cedula.set(personaDB[1])
                articulo.descripcion.set(personaDB[2])
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
    def eliminar(self, articulo):
        try:
            deleteSQL = "delete  from articulos where PK_articulo = " + articulo.articulo.get()
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
    def modificar(self, articulo):
        try:
            if(self.validar(articulo)):#se valida que tenga la información

                if(self.exist(articulo)): #si  existe lo modifica
                    articulo.lastUser = "ChGari"
                    updateSQL = "UPDATE articulos  set `PK_FK_cedula` = %s, `descripcion` = %s, `lastUser` = %s, `lastModification` = CURDATE() WHERE `PK_articulo` =  %s"
                    updateValores =  (articulo.cedula.get(),articulo.descripcion.get(),articulo.lastUser, articulo.articulo.get())
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
    


        
        