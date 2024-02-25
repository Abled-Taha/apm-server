import json

class Config(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
  
  # Loading Config File
  def readConfig(self):
    with open(f'{self.BASE_DIR}/../config.json', 'r') as f:
      self.config = json.load(f)