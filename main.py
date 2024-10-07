import os
import subprocess
from api.Config import Config as ConfigClass

# Setting up Config
BASE_DIR = "./api"
ConfigObj = ConfigClass(BASE_DIR)
ConfigObj.readConfig()

# Running wsgi server
os.chdir("./api")
subprocess.call(["waitress-serve", f"--listen={ConfigObj.server_host}:{ConfigObj.server_port}", "api.wsgi:application"])