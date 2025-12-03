import os, json
from dotenv import load_dotenv

class Config(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
  
  # Loading Config File
  def readConfig(self):
    try:
      load_dotenv(f'{self.BASE_DIR}/../.env')
    except:
      print("Warning: .env File Not Found! Trying to load default session values")
      pass
    try:
      with open(f'{self.BASE_DIR}/../config.json', 'r') as f:
        self.config = json.load(f)
    except:
      raise Exception("Critical: Config File Not Found!")
      
    self.secret_key = os.getenv("secret_key", "django-insecure-czhaxh*di+t*laxo%=bmj8e+89708tgt777ixd3jjl")
    self.db_name = os.getenv("db_name", "apm")
    self.db_username = os.getenv("db_username", "apm")
    self.db_host = os.getenv("db_host", "127.0.0.1")
    self.db_port = int(os.getenv("db_port", "27017"))
    self.db_password = os.getenv("db_password", "apmuserpass")
    self.email_host = os.getenv("email_host", "smtp.gmail.com")
    self.email_port = int(os.getenv("email_port", "587"))
    self.email_host_user = os.getenv("email_host_user", "")
    self.email_host_password = os.getenv("email_host_password", "")

    self.docs_enabled = self.config["docs_enabled"]
    self.debug = self.config["debug"]
    self.allowed_hosts = self.config["allowed_hosts"]
    self.db_srv = self.config["db_srv"]
    self.server_host = self.config["server_host"]
    self.server_port = self.config["server_port"]
    self.username_min_length = self.config["username_min_length"]
    self.username_max_length = self.config["username_max_length"]
    self.password_min_length = self.config["password_min_length"]
    self.password_max_length = self.config["password_max_length"]
    self.sessionId_length = self.config["sessionId_length"]
    self.salt_length = self.config["salt_length"]
    self.max_sessions = self.config["max_sessions"]
    self.pp_width = self.config["pp_width"]
    self.pp_height = self.config["pp_height"]
    self.email_verification = self.config["email_verification"]