class Categoria():

  def __init__(self,id_categoria=None ,nombre_cat= None):
    self.id_categoria = id_categoria
    self.nombre_cat = nombre_cat

  def to_JSON(self):
    return {
      'id_categoria': self.id_categoria,
      'nombre_cat': self.nombre_cat,
    }