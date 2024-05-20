class Cliente():

  def __init__(self, rut= None, nombre= None, correo= None, contraseña= None):
    self.rut = rut
    self.nombre = nombre
    self.correo = correo
    self.contraseña = contraseña

  def to_JSON(self):
    return {
      'rut': self.rut,  
      'nombre': self.nombre,
      'correo': self.correo,
      'contraseña': self.contraseña
  }