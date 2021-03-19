
class Menu():    
    def __init__(self):
        self.condicion_booleana = True

    def desplegar(self):
        seleccion = input(" 1) Para agregar un contacto \n 2) Para buscar un contacto \n 3) Para eliminar un contacto \n 4) Para ver todos los contactos \n 5) Para salir  \n Ingrese su eleccion: " )
        print("\n")

        if seleccion == '1':
            return 'Agregar'
        if seleccion == '2':
            return 'Buscar'
        if seleccion == '3':             
            return 'Eliminar'
        if seleccion == '4':
            return 'Ver'
        if seleccion == '5':
            return 'Salir'

    def solicitar_contacto(self):
        contacto = {
                "cedula" : input('Cedula: '),      
                "nombre" : input('Nombre \n'),
                "apellido_1" : input('1er Apellido: \n'),     
                "apellido_2" : input('2nd Apellido: \n'),    
                "edad" : input('Edad: \n'),     
                "correo" : input('Correo: \n'),     
                "telefono_1" : input('1er Telefono: \n'),    
                "telefono_2" : input('2nd Telefono: \n'), 
            }
        return Contacto(contacto)
         

class Contacto():
    def __init__(self, contacto):
        self.cedula = contacto['cedula'] 
        self.nombre = contacto['nombre'] 
        self.apellido_1 = contacto['apellido_1'] 
        self.apellido_2 = contacto['apellido_2'] 
        self.edad = contacto['edad'] 
        self.correo = contacto['correo']  
        self.telefono_1 = contacto['telefono_1']  
        self.telefono_2 = contacto['telefono_2'] 
        self.direccion = Direccion()   
            
    def ver_datos_contacto(self):
        datos_contacto = {
                        "cedula" : self.cedula,
                        "nombre" : self.nombre, 
                        "apellido_1" : self.apellido_1, 
                        "apellido_2" : self.apellido_2, 
                        "edad" : self.edad, 
                        "correo" : self.correo,
                        "telefono_1" : self.telefono_1, 
                        "telefono_2" : self.telefono_2,
                        "direccion" : self.direccion.ver_direccion(),
                   }
        return datos_contacto

class Direccion:
    def __init__(self,):
        self.pais = input('Pais: ')     
        self.provincia =input('Provincia: ')     
        self.canton = input('Canton: ')     
        self.distrito = input('Distrito: ')     
        self.barrio = input('Barrio: ') 

    def ver_direccion(self):
        datos_dirreccion = {
                        "pais" : self.pais,
                        "provincia" : self.provincia, 
                        "distrito" : self.distrito, 
                        "barrio" : self.barrio,
                    }
        return datos_dirreccion        

class Admin():
    def __init__(self):
        self.nombre = input('Cedula: ')      
        self.apellido = input('Apellido \n')
        self.edad = input('Edad: \n')     
        self.correo = input('Correo: \n')     
        self.telefono = input('telefono: \n')     
        self.estado = input('estado: \n')     
        self._lista_contactos = []

    def agregar_contacto(self, contacto):
         self._lista_contactos.append(contacto)
        
    def buscar_contacto_por_nombre(self, nombre):
        print("BUSCAR==NOMBRE==CONTACTO")

        posicion = 0
        while posicion < len(self._lista_contactos):
            if self._lista_contactos[posicion].nombre in nombre:
                contacto = self._lista_contactos[posicion]
                return contacto
            posicion = posicion + 1

        print("Error buscando nombre:  ", nombre)

    def buscar_contacto_por_apellido(self, apellido):
        print("BUSCAR==APELLIDO==CONTACTO")

        posicion = 0
        while posicion < len(self._lista_contactos):
            if self._lista_contactos[posicion].apellido_1 in apellido:
                contacto = self._lista_contactos[posicion]
                return contacto
            posicion = posicion + 1

        print("Error buscando apellido:  ", apellido)

    def eliminar_contacto_nombre(self, nombre):
        print("ELIMINAR==NOMBRE==CONTACTO")

        if len(nombre)!=0:
            contacto_buscado = self.buscar_contacto_por_nombre(nombre_apellido)

        if contacto_buscado:
            posicion = self._lista_contactos.index(contacto_buscado)
            cedula_ingresada = input("Ingrese la cedula del contacto para eliminarlo: \n")

            if contacto_buscado.cedula == cedula_ingresada:
                return self._lista_contactos.pop(posicion)
        else:
            print("Error Eliminando:  ", nombre)

    def eliminar_contacto_apellido(self, apellido):
        print("ELIMINAR==APELLIDO==CONTACTO")

        if len(apellido)!=0:
            contacto_buscado = self.buscar_contacto_por_apellido(apellido)

        if contacto_buscado:
            posicion = self._lista_contactos.index(contacto_buscado)
            cedula_ingresada = input("Ingrese la cedula del contacto para eliminarlo: \n")

            if contacto_buscado.cedula == cedula_ingresada:
                return self._lista_contactos.pop(posicion)
        else:
            print("Error Eliminando:  ", apellido)


    def ver_datos_admin(self):
        datos_admin = {
                        "nombre" : self.nombre,
                        "apellido" : self.apellido, 
                        "edad" : self.edad, 
                        "correo" : self.correo, 
                        "telefono" : self.telefono, 
                        "estado" : self.estado,
                        "_lista_contactos" : len(self._lista_contactos),
                    }
        print("\nLOS DATOS DE ADMIN SON: ", datos_admin, "\n")

    def ver_mis_lista_contactos(self):
        print("LISTA--DE--CONTACTOS\n\n")

        posicion = 0
        while posicion < len(self._lista_contactos):
            print("Contacto # ", self._lista_contactos[posicion].ver_datos_contacto(), "\n\n")
            posicion = posicion + 1

        print("---FIN---DE---LISTA---\n\n")

class Sistema():
    def _init__(self):
        pass

    def pedir_nombre_apellido(self):
        seleccion = int(input(" 1) Buscar por Nombre \n 2) Buscar por Apellido  \n  " ))
        resultado = {"seleccion" : seleccion,
                        "nombre_o_apellido": ""}

        if seleccion == 1:
            nombre = input(" ---Ingrese un Nombre \n " )
            resultado['nombre_o_apellido'] = nombre
        if seleccion == 2:
                apellido = input(" ---Ingrese un Apellido  \n  " )
                resultado['nombre_o_apellido'] = apellido
        return resultado


    def agregar_contacto(self, admin, contacto):
        admin.agregar_contacto(contacto)
        print("---CONTACTO---AGREGADO! ", contacto.nombre, contacto.apellido_1)

    def buscar_contacto(self, admin, resultado):
        if resultado['seleccion'] == 1:
            contacto = admin.buscar_contacto_por_nombre(resultado['nombre_o_apellido'])
        else:
            contacto = admin.buscar_contacto_por_apellido(resultado['nombre_o_apellido'])

        print("---CONTACTO---ENCONTRADO ", contacto.nombre, contacto.apellido_1)

    def eliminar_contacto(self, admin, resultado):
        if resultado['seleccion'] == 1:
            contacto_eliminado = admin.eliminar_contacto_nombre(resultado['nombre_o_apellido'])
        else:
            contacto_eliminado = admin.eliminar_contacto_apellido(resultado['nombre_o_apellido']) 

        print("---CONTACTO---ELIMINADO ", contacto_eliminado.nombre, contacto_eliminado.apellido_1)

    def ver_lista_contactos(self, admin):
        admin.ver_mis_lista_contactos()

    def terminar(self):
        exit()

    def correr(self):
        datos = {'bandera' : True,
                'opcion' : 0 ,
                'contacto' : '' }

        admin = Admin()
        admin.ver_datos_admin()

        while datos['bandera'] == True: # CICLO DEL SISTEMA
            menu = Menu()
            datos['opcion'] = menu.desplegar()

            if datos['opcion'] == 'Agregar':
                contacto = menu.solicitar_contacto()
                self.agregar_contacto(admin, contacto)

            if datos['opcion'] == 'Buscar':
                resultado = self.pedir_nombre_apellido()
                self.buscar_contacto(admin, resultado)

            if datos['opcion'] == 'Eliminar':
                resultado = self.pedir_nombre_apellido()
                self.eliminar_contacto(admin, resultado)

            if datos['opcion'] == 'Ver':
                self.ver_lista_contactos(admin)

            if datos['opcion'] == 'Salir':
                self.terminar()
                datos['bandera']= False

# Aqui se corre el sistema con los objetos personalizados Menu, Admin, Contacto
sistema = Sistema()
sistema.correr()
