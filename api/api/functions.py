import swiftcrypt
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

def formValidationCreateUser(email, password, rePassword):
  # Does 'password' and 'rePassword' match and are not empty?
  if password != rePassword:
    return(False, "Passwords do not match")

  # Does verfication of 'password' parameter
  if password == "" or len(password) < 6:
    return(False, "Password not acceptable, create a strong Password")
  
  # Does verification of 'email' parameter
  if email.endswith("@gmail.com") == False and email.endswith("@gmail.com ") == False:
    return(False, "Enter a GMAIL address")
  
  # Is this Email already registered?
  if colUsers.find_one({'email':email}) != None:
    return(False, "An account already exists with the same Email")

  return(True, "Succeeded")

def createUser(email, username, password, rePassword):
  isValid, error = formValidationCreateUser(email, password, rePassword)
  
  salt = swiftcrypt.Salts().generate_salt(16)
  passwordHash = swiftcrypt.Hash().hash_password(password, salt, "sha256")
  
  if isValid:
    colUsers.insert_one({'email':email, 'username':username, 'salt':salt, 'passwordHash':passwordHash})
  
  return(isValid, error)