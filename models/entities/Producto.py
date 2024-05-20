class Producto():

  def __init__(self, codigo_prod= None, nombre_prod= None,valor= None, stock= None, id_categoria= None,id_marca= None, id_estado= None, id_sucursal= None):
    self.codigo_prod = codigo_prod
    self.nom_prod = nombre_prod
    self.valor = valor
    self.stock = stock
    self.id_categoria = id_categoria
    self.id_marca = id_marca
    self.id_estado = id_estado
    self.id_sucursal = id_sucursal
  def to_JSON(self):
    return {
      'codigo_prod': self.codigo_prod,
      'nombre_prod': self.nom_prod,
      'valor': self.valor,
      'stock': self.stock,  
      'id_categoria': self.id_categoria,
      'id_marca': self.id_marca,
      'id_estado': self.id_estado,
      'id_sucursal': self.id_sucursal
    }
#upgrade con parametro de codigo de producto, en el json se entrega el codigo y que se va a cambiar (idestado)