class Vendedor():

  def __init__(self, correo_vend= None, nombre_vend= None,id_categoria= None):
    self.correo_vend = correo_vend
    self.nombre_vend = nombre_vend
    self.id_categoria = id_categoria
  def to_JSON(self):
    return {
      'correo_vend': self.correo_vend,
      'nombre_vend': self.nombre_vend,
      'id_categoria': self.id_categoria,
    }
