from flask import Blueprint, jsonify, request
from models.ProductoModel import ProductoModel

main = Blueprint("producto_blueprint", __name__)


@main.route("/")
def Productos():
  try:
    prod = ProductoModel.Productos()
    return jsonify(prod)
  except Exception as ex:
    return jsonify({"message get": str(ex)}), 500


@main.route("/Estado/{<int:id_estado>}")
def Productos_x_estado(id_estado):
  try:
    prod = ProductoModel.Productos_x_estado(id_estado)
    return jsonify(prod)
  except Exception as ex:
    return jsonify({"message get": str(ex)}), 500


@main.route("/Categoria/<int:id_categoria>")
def Productos_x_categoria(id_categoria):
  try:
    prod = ProductoModel.Productos_x_categoria(id_categoria)
    return jsonify(prod)
  except Exception as ex:
    return jsonify({"message get": str(ex)}), 500


@main.route("/Sucursal/<string:codigo_prod>")
def Productos_x_sucursal(codigo_prod):
  try:
    prod = ProductoModel.Productos_x_sucursal(codigo_prod)
    return jsonify(prod)
  except Exception as ex:
    return jsonify({"message get": str(ex)}), 500


@main.route("/Cambiar_estado", methods=['PUT'])
def Cambiar_estado():
  try:
    data_to_update = {
      'id_estado': request.json.get('id_estado'),
      'codigo_prod': request.json.get('codigo_prod')
    }
    affected_rows = ProductoModel.Cambiar_estado(data_to_update)
    if affected_rows == 1:
      return jsonify({"msg": "Estado de producto actualizado"})
    else:
      return jsonify({"message":
                      "No se encontró Producto para actualizar"}), 404
  except Exception as ex:
    return jsonify({"message get": str(ex)}), 500


@main.route("/Historial_precios/<string:codigo_prod>", methods=['GET'])
def historial_precios_producto(codigo_prod):
  try:
    historial_precios = ProductoModel.historial_precio_prod(codigo_prod)
    if historial_precios:
      return jsonify(historial_precios), 200
    else:
      return jsonify(
        {"message":
         "No se encontró historial de precios para el producto"}), 404
  except Exception as ex:
    return jsonify({"message": str(ex)}), 500
