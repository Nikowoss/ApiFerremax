class Contacto:
  def __init__(self,fecha=None ,descripcion= None ,rut= None, correo= None ,id_estado_correo= None):
    self.fecha = fecha
    self.descripcion = descripcion
    self.rut = rut
    self.correo = correo
    self.id_estado_correo = id_estado_correo

  def to_JSON(self):
    return {
      'fecha': self.fecha,
      'descripcion': self.descripcion,
      'rut': self.rut,
      'correo': self.correo,
      'id_estado_correo': self.id_estado_correo,
    }