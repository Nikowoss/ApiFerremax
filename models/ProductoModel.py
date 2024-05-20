from database.db import get_connection
from models.entities.Producto import Producto
from models.entities.Sucursal import Sucursal


class ProductoModel():

    @classmethod
    def Productos(cls):
        try:
            cx = get_connection()
            prod = []
            with cx.cursor() as cursor:
                cursor.execute(
                    "SELECT producto.codigo_prod, nom_prod, valor, stock.stock, id_estado, id_categoria, id_marca, stock.id_sucursal FROM producto JOIN stock ON producto.codigo_prod = stock.codigo_prod"
                )
                resultset = cursor.fetchall()
                for row in resultset:
                    pr = Producto(row[0], row[1], row[2], row[3], row[4],
                                  row[5], row[6], row[7])
                    prod.append(pr.to_JSON())
            # La conexión se cierra automáticamente al salir del bloque "with"
            return prod
        except Exception as ex:
            return str(ex)

    @classmethod
    def Productos_x_estado(cls, id_estado):
        try:
            cx = get_connection()
            prod = []
            with cx.cursor() as cursor:
                cursor.execute(
                    "SELECT producto.codigo_prod, producto.nom_prod, producto.valor, stock.stock, producto.id_categoria, producto.id_marca, producto.id_estado, stock.id_sucursal FROM producto JOIN stock ON producto.codigo_prod = stock.codigo_prod WHERE producto.id_estado = %s",
                    (id_estado, ))
                resultset = cursor.fetchall()
                for row in resultset:
                    pr = Producto(row[0], row[1], row[2], row[3], row[4],
                                  row[5], row[6], row[7])
                    prod.append(pr.to_JSON())
            return prod
        except Exception as ex:
            return str(ex)

    @classmethod
    def Productos_x_categoria(cls, id_categoria):
        try:
            cx = get_connection()
            prod = []
            with cx.cursor() as cursor:
                cursor.execute(
                    "SELECT producto.codigo_prod, producto.nom_prod, producto.valor, stock.stock, producto.id_categoria, producto.id_marca, producto.id_estado, stock.id_sucursal FROM producto JOIN stock ON producto.codigo_prod = stock.codigo_prod WHERE producto.id_categoria = %s",
                    (id_categoria, ))
                resultset = cursor.fetchall()
                for row in resultset:
                    pr = Producto(row[0], row[1], row[2], row[3], row[4],
                                  row[5], row[6], row[7])
                    prod.append(pr.to_JSON())
            return prod
        except Exception as ex:
            return str(ex)

    @classmethod
    def Productos_x_sucursal(cls, codigo_prod):
        try:
            cx = get_connection()
            prod = []
            with cx.cursor() as cursor:
                cursor.execute(
                    "SELECT stock.id_sucursal FROM producto JOIN stock ON producto.codigo_prod = stock.codigo_prod WHERE producto.codigo_prod = %s",
                    (codigo_prod, ))
                resultset = cursor.fetchall()
                for row in resultset:
                    pr = Sucursal(row[0])
                    prod.append(pr.to_JSON())
            return prod
        except Exception as ex:
            return str(ex)

    @classmethod
    def Cambiar_estado(cls, data_to_update):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                update_query = (
                    "UPDATE producto SET id_estado = %s WHERE codigo_prod = %s"
                )
                update_values = (data_to_update['id_estado'], data_to_update['codigo_prod'])
                cursor.execute(update_query, update_values)
                affected_rows = cursor.rowcount
                cx.commit()
                cx.close()
                return affected_rows
        except Exception as ex:
            return Exception(ex)

    @classmethod
    def historial_precio_prod(cls, codigo_prod):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                query = (
                    "SELECT venta.fecha, detalle_venta.valor "
                    "FROM detalle_venta "
                    "INNER JOIN venta ON detalle_venta.id_venta = venta.id_venta "
                    "WHERE detalle_venta.codigo_prod = %s")
                cursor.execute(query, (codigo_prod, ))
                result = cursor.fetchall()
                cx.close()
                return result
        except Exception as ex:
            return str(ex)
            
    @classmethod
    def Cambiar_stock(cls, data):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                update_query = (
                    "UPDATE stock SET stock = (stock - %s) WHERE codigo_prod = %s AND id_sucursal = %s"
                )
                update_values = (
                    data.get('cantidad'),
                    data.get('codigo_prod'),
                    data.get('id_sucursal')
                )
                cursor.execute(update_query, update_values)
                affected_rows = cursor.rowcount
                cx.commit()
                cx.close()
                return affected_rows
        except Exception as ex:
            return Exception(ex)
    
    @classmethod
    def Saber_Stock(cls, codigo_prod, id_sucursal):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT stock FROM stock WHERE codigo_prod = %s AND id_sucursal = %s", (codigo_prod, id_sucursal,))
                result = cursor.fetchone() 
                if result:
                    stock = result[0]
                    cx.close()
                    return stock
                else:
                    cx.close()
                    return None  
        except Exception as ex:
            return ex
            
    def Venta(cls, datos_venta):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                insert_query = (
                    "INSERT INTO venta (id_venta,monto_final, fecha, metodo_de_pago, rut) "
                    "VALUES (%s,%s, %s, %s, %s)")
                insert_values = (
                    datos_venta.get('id_venta'),
                    datos_venta.get('monto_final'),
                    datos_venta.get('fecha'),
                    datos_venta.get('metodo_de_pago'),
                    datos_venta.get('rut'))
                cursor.execute(insert_query, insert_values)
                cx.commit()
                inserted_id = cursor.lastrowid
                return {"inserted_id": inserted_id}
        except Exception as ex:
            cx.rollback()
            return {"error": str(ex)}
        finally:
            cx.close()
