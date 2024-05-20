class Precio():

  def __init__(self, id_precio= None,fecha= None,valor= None):
    self.id_precio = id_precio
    self.fecha = fecha
    self.valor = valor

  def to_JSON(self):
    return {
      'fecha': self.fecha,
      'valor': self.valor,
    }
