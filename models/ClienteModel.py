from database.db import get_connection
from werkzeug.security import check_password_hash
from models.entities.Contacto import Contacto
from models.entities.Vendedor import Vendedor
from models.entities.Cliente import Cliente
import time

class ClienteModel():
  @classmethod
  def Crear_Cuenta(self, cliente):
    try:
      cx = get_connection()
      with cx.cursor() as cursor:
        cursor.execute(
          "INSERT INTO Cliente (rut, nombre, correo, contraseña) VALUES (%s, %s, %s, %s)",
          (cliente.rut, cliente.nombre, cliente.correo,cliente.contraseña,))
        affected_rows = cursor.rowcount
        cx.commit()
      cx.close()
      return affected_rows
    except Exception as ex:
      return Exception(ex)
      
  @classmethod
  def login(self, cliente):
    try:
      cx = get_connection()
      with cx.cursor() as cursor:
        cursor.execute("SELECT contraseña FROM cliente WHERE correo=%s",
                     (cliente.correo,))
        resultset = cursor.fetchone()
        if resultset is not None:
          if check_password_hash(resultset[0], cliente.contraseña):
            return True
          else:
            raise Exception("Correo o contraseña incorrectaaaa")
        else:
          raise Exception("Correo o contraseña incorrectaa")
    except Exception as ex:
      raise Exception(ex)
      
        
  @classmethod
  def enviar_correo_duda_vend(cls,cliente,corre):
    affected_rows = 0
    try:
      hora_actual = time.time()
      estructura_tiempo_actual = time.localtime(hora_actual)
      hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_actual)

      cx = get_connection()
      
      with cx.cursor() as cursor:
        cursor.execute("INSERT INTO Contacto (fecha_hora , descripcion, rut, correo , id_estado_correo) VALUES (%s, %s, %s, %s, 1)",(hora_actual, cliente.descripcion, cliente.rut, corre))
        affected_rows = cursor.rowcount
        cx.commit()
      return affected_rows
    except Exception as ex:
      return str(ex)
    finally:
      if cx is not None:
        cx.close() 
    
  def ver_correo(rut):
    try:
      #Obtener la conexion
      cx = get_connection()
      respuesta = []
      with cx.cursor() as cursor:
        cursor.execute(
          "SELECT fecha_hora, descripcion, rut, correo , id_estado_correo FROM Contacto WHERE rut = %s ORDER BY fecha_hora DESC", (rut,))
        resultset = cursor.fetchall()
        for row in resultset:
          res = Contacto(row[0], row[1], row[2], row[3], row[4])
          respuesta.append(res.to_JSON())
      cx.close()
      return respuesta
    except Exception as ex:
      return Exception(ex)

  def ver_clientes():
    try:
      #Obtener la conexion
      cx = get_connection()
      respuesta = []
      with cx.cursor() as cursor:
        cursor.execute(
          "SELECT rut,nombre,correo FROM cliente")
        resultset = cursor.fetchall()
        for row in resultset:
          res = Cliente(row[0], row[1], row[2])
          respuesta.append(res.to_JSON())
      cx.close()
      return respuesta
    except Exception as ex:
      return Exception(ex)


  def select_vendedor_x_cat(id_cat):
    try:
      cx = get_connection()
      respuesta = []
      with cx.cursor() as cursor:
        cursor.execute(
          "SELECT vendedor.correo,vendedor.nombre,categoria.id_categoria FROM vendedor, categoria WHERE vendedor.id_categoria = categoria.id_categoria AND vendedor.id_categoria = %s", (id_cat,))
        resultset = cursor.fetchall()
        for row in resultset:
          res = Vendedor(row[0], row[1], row[2])
          respuesta.append(res.to_JSON())
      cx.close()
      return respuesta
    except Exception as ex:
      return Exception(ex)

  def Select_rut_cli(correo):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("SELECT rut FROM cliente WHERE correo = %s", (correo,))
            resultset = cursor.fetchone()
            if resultset is not None:
                rut = str(resultset[0])  # Convertir a string
            else:
                rut = None
        cx.close()
        return rut
    except Exception as ex:
        return str(ex)
