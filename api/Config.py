import json

class Config(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
  
  # Loading Config File
  def readConfig(self):
    with open(f'{self.BASE_DIR}/../config.json', 'r') as f:
      self.config = json.load(f)
      
      self.debug = self.config["debug"]
      self.secret_key = self.config["secret_key"]
      self.allowed_hosts = self.config["allowed_hosts"]
      self.db_name = self.config["db_name"]
      self.db_username = self.config["db_username"]
      self.db_host = self.config["db_host"]
      self.db_port = self.config["db_port"]
      self.db_password = self.config["db_password"]
      self.username_min_length = self.config["username_min_length"]
      self.username_max_length = self.config["username_max_length"]
      self.password_min_length = self.config["password_min_length"]
      self.password_max_length = self.config["password_max_length"]
      self.sessionId_length = self.config["sessionId_length"]
      self.salt_length = self.config["salt_length"]
      self.max_sessions = self.config["max_sessions"]