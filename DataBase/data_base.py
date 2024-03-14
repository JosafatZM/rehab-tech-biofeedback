import mysql.connector
import os
import subprocess
import datetime

acceso_bd = {"host": "localhost",
             "user": "root",
             "password": "DataBase98_!",
             "database": "pruebas"
}

# Obtener la ruta de la carpeta del proyecto
carpeta_principal = os.path.dirname(__file__)

# Ruta de la carpeta de respaldo 
respaldo = os.path.join(carpeta_principal, "respaldo")


class BaseDatos:
    # Conexion y cursor
    def __init__(self, **kwargs):
        self.conector = mysql.connector.connect(**kwargs)
        self.cursor = self.conector.cursor()
        self.host = kwargs["host"]
        self.usuario = kwargs["user"]
        self.contrasena = kwargs["password"]
        self.conexion_cerrada = False
        print("Se inicializo la base de datos")

   # Decorador para el cierre del cursor y la base de datos
    def conexion(funcion_parametro):
        def interno(self, *args, **kwargs):
            try:
                if self.conexion_cerrada:
                    self.conector = mysql.connector.connect(
                        host = self.host,
                        user = self.usuario,
                        password = self.contrasena
                    )
                    self.cursor = self.conector.cursor()
                    self.conexion_cerrada = False
                    print("Se abrió la conexión con el servidor.")
                # Se llama a la función externa
                funcion_parametro(self, *args, **kwargs)
            except Exception as e:
              	# Se informa de un error en la llamada
                print(f"Ocurrio un error - {e}")
            finally:
                if self.conexion_cerrada:
                    pass
                else:
                    # Cerramos el cursor y la conexión
                    self.cursor.close()
                    self.conector.close()
                    print("Se cerró la conexión con el servidor.")
                    self.conexion_cerrada = True
            return self.result
        return interno

    # Decorador para comprobar que existe una base de datos
    def comprobar_existencia_bd(funcion_parametro):

        def interno(self, nombre_bd, *args, **kwargs):
             # Verificar que la base de datos existe
            sql = f"SHOW DATABASES LIKE '{nombre_bd}'"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()

            if resultado == None:
                print(f"Estado de la Base de Datos '{nombre_bd}': Inexistente.")
                # 'return' para terminar con la ejecucion del metodo por la inexistencia 
                # de la base de datos
                return
            
            funcion_parametro(self, nombre_bd, *args, **kwargs)

        return interno


    @conexion
    def consulta(self, sql):
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
    
    
    # Muestra las bases de datos del servidos
    @conexion
    def mostrar_bd(self):
        try:
            # Se informa de que se están obteniendo las bases de datos
            print("Aquí tienes el listado de las bases de datos del servidor:")
            # Realiza la consulta para mostrar las bases de datos
            self.cursor.execute("SHOW DATABASES")
            resultado = self.cursor.fetchall()
            # Recorre los resultados y los muestra por pantalla
            for bd in resultado:
                print(f"-{bd[0]}.")
        except:
            # Si ocurre una excepción, se avisa en la consola
            print("No se pudieron obtener las bases de datos. Comprueba la conexión con el servidor.")
             
    # Crear un respaldo de la base de datos
    @conexion
    @comprobar_existencia_bd
    def respaldo_bd(self, nombre_bd):

        #obtener la fecha y hora del respaldo 
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        with open(f'{respaldo}/{nombre_bd}_{fecha_hora}.sql', 'w') as out:
            subprocess.Popen(fr'"C:\Program Files\MySQL\MySQL Workbench 8.0\"mysqldump --user=root --password={self.contrasena} --databases {nombre_bd}',
                             shell=True, stdout=out)
            
        print(f"Se creo la copia de seguridad '{nombre_bd}_{fecha_hora}.sql''")


    # Método para actualizar registros en una tabla
    @conexion
    @comprobar_existencia_bd
    def actualizar_registro(self, nombre_bd, nombre_tabla, columnas, condiciones):
        try:
          	# Se selecciona la base de datos
            self.cursor.execute(f"USE {nombre_bd}")

            # Crear la instrucción de actualización
            sql = f"UPDATE {nombre_tabla} SET {columnas} WHERE {condiciones}"
            # Se ejecuta la instrucción de actualización y se hace efectiva
            self.cursor.execute(sql)
            self.conector.commit()
            print("Se actualizó el registro correctamente.")
        except:
            print("Ocurrió un error al intentar actualizar el registro.")