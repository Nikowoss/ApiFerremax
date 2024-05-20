from database.db import get_connection
from models.entities.Vendedor import Vendedor
from models.entities.Contacto import Contacto
import time

class VendedorModel:
  
  @classmethod
  def login(self, vendedor):
    try:
      cx = get_connection()
      with cx.cursor() as cursor:
        cursor.execute("SELECT correo FROM vendedor WHERE correo=%s",
                     (vendedor.correo_vend,))
        resultset = cursor.fetchone()
        if resultset is not None:
            return True
        else:
          raise Exception("Correo o contraseña incorrecto")
    except Exception as ex:
      raise Exception(ex)



  @classmethod
  def env_correo_vend(cls,con,cor,rut):
    affected_rows = 0
    try:
      hora_actual = time.time()

      estructura_tiempo_actual = time.localtime(hora_actual)

      hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_actual)

      fecha = cls.fecha_msg(rut,cor)
      cx = get_connection()
      with cx.cursor() as cursor:
          cursor.execute(
            "INSERT INTO Contacto (fecha_hora, descripcion, rut, correo, id_estado_correo) VALUES (%s, %s, %s, %s, '2')",(hora_actual, con.descripcion, rut, cor))
          affected_rows = cursor.rowcount
      cx.commit()
      with cx.cursor() as cursor:
        cursor.execute(
          "UPDATE Contacto SET id_estado_correo = '2' WHERE id_estado_correo = '1' AND rut = %s AND correo = %s AND fecha_hora = %s",(rut,cor,fecha))
      cx.commit()
      cx.close()
      return affected_rows
    except Exception as ex:
      return str(ex)

  def fecha_msg(rut,cor):
      try:
        cx = get_connection()
        with cx.cursor() as cursor:
          cursor.execute(
            "SELECT MIN(fecha_hora) FROM contacto WHERE rut = %s AND correo = %s AND id_estado_correo = '1' ORDER BY 1 DESC",(rut,cor))
          resultset = cursor.fetchone()
          if resultset is not None:
            fecha = resultset[0]
          cx.close()
        return fecha
      except Exception as ex:
        return str(ex)
      
  #Este permite ver los correos por vendedor
  @classmethod
  def ver_correo_vend(cls,cor):
    try:
      cx = get_connection()
      correos = []
      with cx.cursor() as cursor:
        cursor.execute(
          "SELECT fecha_hora, descripcion, rut, correo , id_estado_correo FROM contacto WHERE correo = %s ORDER BY 1 DESC",(cor,))
        resultset = cursor.fetchall()
        for row in resultset:
          correo = Contacto(row[0], row[1], row[2], row[3], row[4])
          correos.append(correo.to_JSON())
      cx.close()
      return correos
    except Exception as ex:
      return str(ex)

  #Este permite ver los correos por vendedor y por id como filtro si esque estan respondidos o no 
  @classmethod
  def ver_correo_vend_x_id(cls,cor,id_est):
    try:
      cx = get_connection()
      correos = []
      with cx.cursor() as cursor:
        cursor.execute(
          "SELECT fecha_hora, descripcion, rut, correo , id_estado_correo FROM contacto WHERE correo = %s AND id_estado_correo = %s ORDER BY 1 DESC",(cor,id_est))
        resultset = cursor.fetchall()
        for row in resultset:
          correo = Contacto(row[0], row[1], row[2], row[3], row[4])
          correos.append(correo.to_JSON())
      cx.close()
      return correos
    except Exception as ex:
      return str(ex)

  
  #generar crear vendedor
  @classmethod
  def Crear_Cuenta(cls,vend):
    try:
      cx = get_connection()
      with cx.cursor() as cursor:
        cursor.execute("INSERT INTO Vendedor (correo, nombre, id_categoria) VALUES (%s, %s, %s)",(vend.correo_vend, vend.nombre_vend, vend.id_categoria))
        affected_rows = cursor.rowcount
        cx.commit()
      return affected_rows
    except Exception as ex:
      return str(ex)
    finally:
      if cx is not None:
        cx.close() 
