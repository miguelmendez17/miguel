"""Se debe crear un sistema para manejar tu lista de contactos.


A.
El sistema debe solicitar SOLAMENTE al inicio tus datos personales y 
registrar tu cuenta como la dueña de la lista de contactos. 
Dentro de los datos personales debe consultar mi nombre, 
apellido, edad, correo electrónico, teléfono y estado civil.

B.
El sistema debe tener un menú con las siguientes opciones:

1. Ver mis datos (el dueño de la cuenta)
En esta opción se debe desplegar toda mi información que fue solicitada al inicio en el punto A.

2. Ingresar un contacto a mi lista
2.1
Al contacto de la lista se le debe solicitar cédula, 
nombre, primer apellido, segundo apellido, edad, correo electrónico,
 teléfono, segundo teléfono y dirección.
2.2
Se debe usar una Clase para manejar la información del contacto 
y se debe usar una Clase para la dirección. La dirección debe 
tener en cuenta el país, la provincia, el cantón, distrito y nombre del barrio.

2.3
Se debe crear una lista y en esa lista guardar los contactos como Objetos, 
y de la misma manera se debe poder acceder a los objetos por medio de esta misma lista

3. Buscar un contacto de mi lista por nombre o por apellido
3.1
Por medio de la lista se debe buscar el objeto de tipo contacto 
que cumpla con el término de búsqueda que es el nombre o el apellido del contacto.

3.2
Se debe solicitar al usuario que ingrese el nombre o el apellido del contacto a buscar


4. Eliminar un contacto de mi lista
4.1
Se debe buscar un usuario por su cédula y al encontrarlo se debe eliminar de la lista
4.2
Se debe solicitar al usuario que ingrese el nombre o el apellido del contacto a buscar


5. Ver la lista de contactos
5.1
Se debe hacer un recorrido de la lista e imprimir los datos de TODOS los contactos que pertenecen
 a la lista, se debe desplegar TODA su información.
5.2
Se debe realizar un ciclo

6. Salir.



C. Otras Observaciones.
El código debe tener un orden con la identación adecuada. 5pts.
El nombre de las variables, funciones, parámetros debe tener sentido 
y no nombres que no se relacionen con el propósito con el que fueron creados. 5pts.
Aunque fue explicado en detalle el problema, se deben crear Clases, 
mínimo una para el dueño de la cuenta y otra para manejar el contacto. 20pts.
Deben usar ciclos cuando sea necesario, al menos 2 son necesarios para resolver el problema. 20pts.
Deben crear funciones además del constructor de la clase. 10pts.
El sistema debe tener un menú que va funcionar y va desplegar las 
opciones hasta que se solicite la opción de salir. 10pts.
El sistema debe funcionar, no voy a realizar validaciones de datos, 
pero al realizar alguna de las funciones del menu deben ejecutarse sin problema 30pts."""