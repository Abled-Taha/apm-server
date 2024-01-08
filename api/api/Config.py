import json

class Config():
  def __init__(self):
    with open('config/config.json') as configFile:
      self.configData = json.load(configFile)

      self.debug = self.configData['debug']
      self.secretKey = self.configData['secretKey']
      
      self.hostDB = self.configData['hostDB']
      self.portDB = self.configData['portDB']
      self.nameDB = self.configData['nameDB']
      self.username = self.configData['username']
      self.pwd = self.configData['pwd']