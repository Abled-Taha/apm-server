import swiftcrypt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . import dbHandler
from . import Config as ConfigFile

Config = ConfigFile.Config()
supplyGUIResponse = Config.supplyGUIResponse

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
  # Does verification of 'email' parameter
  if email.endswith("@gmail.com") == False:
    return(False, "Enter a GMAIL address")
  
  # Does verfication of 'password' parameter
  if password == "" or len(password) < 6:
    return(False, "Password not acceptable, create a strong Password")
  
  # Does 'password' and 'rePassword' match?
  if password != rePassword:
    return(False, "Passwords do not match")

  # Is this Email already registered?
  if colUsers.find_one({'email':email}) != None:
    return(False, "An account already exists with the same Email")

  return(True, "Succeeded")

def formValidationLoginUser(email, password):
  # Does verification of 'email' parameter
  if email.endswith("@gmail.com") == False:
    return(False, "Enter a GMAIL address", None)
  
  # Does verfication of 'password' parameter
  if password == "" or len(password) < 6:
    return(False, "Incorrect Credentials", None)

  # Is this Email registered?
  account = colUsers.find_one({'email':email})
  if account == None:
    return(False, "No account exists with this Email", None)

  return(True, "Succeeded", account)

def createUser(email, username, password, rePassword):
  isValid, error = formValidationCreateUser(email, password, rePassword)
  
  salt = swiftcrypt.Salts().generate_salt(16)
  passwordHash = swiftcrypt.Hash().hash_password(password, salt, "sha256")
  
  if isValid:
    try:
      colUsers.insert_one({'email':email, 'username':username, 'salt':salt, 'passwordHash':passwordHash})
    except Exception as e:
      error = e
      return(isValid, error)
    User.objects.create_user(username=username, email=email, password=passwordHash)
    error = "Account Created!"
  
  return(isValid, error)

def loginUser(request, email, password):
  isValid, error, account = formValidationLoginUser(email, password)
  
  if isValid:
    username = account["username"]
    salt = account["salt"]
    passwordHash = account["passwordHash"]
    checkPassword = swiftcrypt.Checker().verify_password(password, passwordHash, salt, "sha256")
  
    if checkPassword:
      user = authenticate(username=username, password=passwordHash)
      login(request, user)
      error = "Logged In"
      return(isValid, error, account)
  
  error = "Incorrect Credentials"
  return(isValid, error, account)