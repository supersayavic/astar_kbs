from lib.Feld import Feld

class Ebene:
  def __init__(self, input):
      self.felder = list(list((Feld(item)) for item in line.rstrip("\n\r").split(";")) for line in input)