from flask import Blueprint, jsonify, request
from models.VendedorModel import VendedorModel
from models.entities.Contacto import Contacto
from models.entities.Vendedor import Vendedor
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token

main = Blueprint("vendedor_blueprint", __name__)

@main.route("/Login", methods=['POST'])
def Login():
  try:
    correo_vend = request.json['correo']
    vendedor = Vendedor(correo_vend=correo_vend)
    affected_rows = VendedorModel.login(vendedor)
    if affected_rows:
      access_token = create_access_token(identity=vendedor.correo_vend)
      return jsonify({ "token": access_token, "user_id": vendedor.correo_vend })
  except Exception as ex:
    return jsonify({"message": str(ex)}), 500
    

#Enviar el correo del vendedor con su correo como parametro, es decir automatico xd
@main.route("/Enviar_correo_vend/{<string:cor>}/{<string:rut>}", methods=['POST'])
def Enviar_correo_vend(cor,rut):
  try:

    descripcion = request.json['descripcion']

    cont = Contacto(descripcion=descripcion)
    affected_rows = VendedorModel.env_correo_vend(cont,cor,rut)
    if affected_rows == 1:
      return jsonify({"msg": "Correo enviado"})
    else:
      print(affected_rows)
      return jsonify({"message": "Error al enviar"}), 500
  except Exception as ex:
    return jsonify({"messageeeeeeeeee": str(ex)}), 500


#Este permite ver los correos solo por el vendedor 
@main.route("/Ver_Correos_vend/{<string:cor>}", methods=['GET'])
@jwt_required() 
def Ver_Correos_vend(cor):
  try:
    correos = VendedorModel.ver_correo_vend(cor)
    return jsonify(correos)
  except Exception as ex:
    print(ex)
    return jsonify({"message get": str(ex)}), 500

#Este permite ver los correos por vendedor y por id como filtro si esque estan respondidos o no 
@main.route("/Ver_Correos_vend_x_id/{<string:cor>}/{<int:id_est>}", methods=['GET'])
def Ver_Correos_vend_x_id(cor,id_est):
  try:
    correos = VendedorModel.ver_correo_vend_x_id(cor,id_est)
    return jsonify(correos)
  except Exception as ex:
    print(ex)
    return jsonify({"message get": str(ex)}), 500


@main.route("/Crear_vendedor", methods=['POST'])
def Crear_vendedor():
  try:
    nombre = request.json['nombre_vend']
    correo_vend = request.json['correo_vend']
    id_categoria = request.json['id_categoria']
    vendedor = Vendedor(nombre_vend=nombre,correo_vend=correo_vend,id_categoria=id_categoria)
    affected_rows = VendedorModel.Crear_Cuenta(vendedor)
    if affected_rows == 1:
      return jsonify({"msg": "Vendedor creado"})
    else:
      print(affected_rows)
      return jsonify({"message": "Error al insertar"}), 500
  except Exception as ex:
    return jsonify({"messageeeeeeeeee": str(ex)}), 500
