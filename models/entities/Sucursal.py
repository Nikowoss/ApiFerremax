class Sucursal():

  def __init__(self, id_sucursal=None, nom_sucursal=None):
    self.id_sucursal = id_sucursal

  def to_JSON(self):
    return {'id_sucursal': self.id_sucursal}
