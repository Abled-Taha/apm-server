from . import dbHandler
from . import Config as ConfigFile

Config = ConfigFile.Config()

client, db, colUsers, colUsersData = dbHandler.connect(hostDB=Config.hostDB, portDB=Config.portDB, nameDB=Config.nameDB, username=Config.username, pwd=Config.pwd)

def readAllUsers():
  dict = {}
  index = 0

  for x in colUsers.find():
    x["_id"] = str(x["_id"])
    dict[f"{index}"] = x

    index += 1
  
  return(dict)