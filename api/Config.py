import os
from dotenv import load_dotenv

class Config(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
  
  # Loading Config File
  def readConfig(self):
    try:
      load_dotenv(f'{self.BASE_DIR}/../.env')
    except:
      pass
      
    self.debug = os.getenv("debug")
    if self.debug == "True":
      self.debug = True
    else:
      self.debug = False
    self.secret_key = os.getenv("secret_key")
    self.allowed_hosts = os.getenv("allowed_hosts").split(",")
    self.db_name = os.getenv("db_name")
    self.db_username = os.getenv("db_username")
    self.db_host = os.getenv("db_host")
    self.db_port = int(os.getenv("db_port"))
    self.db_password = os.getenv("db_password")
    self.db_srv = os.getenv("db_srv")
    if self.db_srv == "True":
      self.db_srv = True
    else:
      self.db_srv = False
    self.server_host = os.getenv("server_host")
    self.server_port = os.getenv("server_port")
    self.username_min_length = int(os.getenv("username_min_length"))
    self.username_max_length = int(os.getenv("username_max_length"))
    self.password_min_length = int(os.getenv("password_min_length"))
    self.password_max_length = int(os.getenv("password_max_length"))
    self.sessionId_length = int(os.getenv("sessionId_length"))
    self.salt_length = int(os.getenv("salt_length"))
    self.max_sessions = int(os.getenv("max_sessions"))
    self.pp_width = int(os.getenv("pp_width"))
    self.pp_height = int(os.getenv("pp_height"))