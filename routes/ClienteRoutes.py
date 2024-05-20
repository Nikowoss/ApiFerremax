from flask import Blueprint, jsonify, request, json
from models.ClienteModel import ClienteModel
from models.entities.Cliente import Cliente
from models.entities.Contacto import Contacto
from werkzeug.security import generate_password_hash

from flask_jwt_extended import create_access_token

main = Blueprint("cliente_blueprint", __name__);

rut_cliente = {}

@main.route("/Login", methods=['POST'])
def Login():
  try:
    correo = request.json['correo']
    contraseña = request.json['contraseña']
    cliente = Cliente(correo=correo, contraseña=contraseña)
    affected_rows = ClienteModel.login(cliente)
    rut = ClienteModel.Select_rut_cli(correo)
    print(rut)
    if affected_rows:
      global rut_cliente
      rut_cliente=rut 
      print(rut_cliente)
      access_token = create_access_token(identity=cliente.correo)
      return jsonify({ "token": access_token, "user_id": cliente.correo })
  except Exception as ex:
    return jsonify({"message": str(ex)}), 500

@main.route("/Crear_Cuenta", methods=['POST'])
def Crear_Cuenta():
  try:
    rut = request.json['rut']
    nombre = request.json['nombre']
    correo = request.json['correo']
    contraseña = request.json['contraseña']
    contraseña = generate_password_hash(contraseña)
    cliente = Cliente(rut=rut,nombre=nombre,correo=correo,contraseña=contraseña)
    affected_rows = ClienteModel.Crear_Cuenta(cliente)
    if affected_rows == 1:
      return jsonify({"msg": "Felicidades Ahora puedes iniciar sesion"})
    else:
      return jsonify({"message": "Error al insertar"}), 500
  except Exception as ex:
    return jsonify({"messageeeeeeeeee": str(ex)}), 500

    
@main.route("/Enviar_correo_a_vend/{<string:corre>}", methods=['POST'])
def Enviar_correo_a_vend(corre):
  try:
    descripcion = request.json['descripcion']
    rut = request.json['rut']
    
    cont = Contacto(descripcion=descripcion,rut=rut)
    affected_rows = ClienteModel.enviar_correo_duda_vend(cont,corre)
    if affected_rows == 1:
      return jsonify({"msg": "Correo enviado"})
    else:
      print(affected_rows)
      return jsonify({"message": "Error al enviar correo"}),500
  except Exception as ex:
    return jsonify({"messageeeeeeeeee": str(ex)}), 500


@main.route("/Ver_correo/{<string:rut>}", methods=['GET'])
def Ver_correo(rut):
  try:
    print(rut)
    correos = ClienteModel.ver_correo(rut)
    print(correos)
    return jsonify(correos)
  except Exception as ex:
    print(ex)
    error_info = {"error_message": str(ex)}
    # Convertir el diccionario a formato JSON
    json_response = json.dumps(error_info)
    return jsonify({"message get": json_response}), 500

@main.route("/Ver_clientes", methods=['GET'])
def Ver_clientes():
  try:
    clientes = ClienteModel.ver_clientes()
    return jsonify(clientes)
  except Exception as ex:
    return jsonify({"message get": str(ex)}), 500



@main.route("/Select_vendedor_x_id/{<int:id_cat>}", methods=['GET'])
def Select_vendedor_x_cat(id_cat):
  try:
    vendedor = ClienteModel.select_vendedor_x_cat(id_cat)
    return jsonify(vendedor)
  except Exception as ex:
    return jsonify({"message get": str(ex)}), 500

