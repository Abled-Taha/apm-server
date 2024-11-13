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
      
    self.debug = os.getenv("debug", "False")
    if self.debug == "True":
      self.debug = True
    else:
      self.debug = False
    self.secret_key = os.getenv("secret_key", "django-insecure-czhaxh*di+t*laxo%=bmj8e+8970)#8tgt&77)7&ixd#3j=j=l")
    self.allowed_hosts = os.getenv("allowed_hosts", "*").split(",")
    self.db_name = os.getenv("db_name", "apm")
    self.db_username = os.getenv("db_username", "apm")
    self.db_host = os.getenv("db_host", "127.0.0.1")
    self.db_port = int(os.getenv("db_port", "27017"))
    self.db_password = os.getenv("db_password", "apmuserpass")
    self.db_srv = os.getenv("db_srv", "False")
    if self.db_srv == "True":
      self.db_srv = True
    else:
      self.db_srv = False
    self.server_host = os.getenv("server_host", "127.0.0.1")
    self.server_port = int(os.getenv("server_port", "8000"))
    self.username_min_length = int(os.getenv("username_min_length", "3"))
    self.username_max_length = int(os.getenv("username_max_length", "10"))
    self.password_min_length = int(os.getenv("password_min_length", "6"))
    self.password_max_length = int(os.getenv("password_max_length", "20"))
    self.sessionId_length = int(os.getenv("sessionId_length", "16"))
    self.salt_length = int(os.getenv("salt_length", "16"))
    self.max_sessions = int(os.getenv("max_sessions", "10"))
    self.pp_width = int(os.getenv("pp_width", "150"))
    self.pp_height = int(os.getenv("pp_height", "150"))