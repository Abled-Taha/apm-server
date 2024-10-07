from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import json
import swiftcrypt
import secrets
import string
from .settings import db, ConfigObj
from . import encryptor

def validateSigninData(email, password):
  account = db.find_one("users", {"email":email})
  if account != None:
    if swiftcrypt.Checker().verify_password(password, account["passwordHash"], account["salt"], "sha256"):
      return(True, {"errorCode":0, "errorMessage":"Success"}, account)
    return(False, {"errorCode":1, "errorMessage":"Incorrect Password"}, account)
  return(False, {"errorCode":1, "errorMessage":"No Account exists with that Email."}, account)

def generateSessionId():
  characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
  sessionId = ''.join(secrets.choice(characters) for i in range(ConfigObj.sessionId_length))
  return(sessionId)

def validateSignupData(email, username, password, rePassword):
  if db.find_one("users", {"email":email}) == None:
    if len(username) >= ConfigObj.username_min_length and len(username) <= ConfigObj.username_max_length and username.isalnum():
      if password == rePassword and len(password) >= ConfigObj.password_min_length and len(password) <= ConfigObj.password_max_length:
        return(True, {"errorCode":0, "errorMessage":"Success"})
      return(False, {"errorCode":1, "errorMessage":f"The passwords must match and must have more than {ConfigObj.password_min_length} and less than {ConfigObj.password_max_length} characters"})
    return(False, {"errorCode":1, "errorMessage":f"The username must have more than {ConfigObj.username_min_length} and less than {ConfigObj.username_max_length} characters"})
  return(False, {"errorCode":1, "errorMessage":"User already exists with this email"})


def validateSession(account, data):
  for entry in account["sessionIds"]:
    if entry["sessionId"] == data["sessionId"]:
      return(True)
  return(False)

def signin(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  else:
    try:
      data = json.loads(request.body)
      isValid, error, account = validateSigninData(data["email"], data["password"])
      
      if isValid:
        sessionId = generateSessionId()
        try:
          sessionName = data["sessionName"]
        except:
          sessionName = ""
        account["sessionIds"].append({"name":sessionName, "sessionId":sessionId})
        if len(account["sessionIds"]) > ConfigObj.max_sessions:
          del account["sessionIds"][0]

        if db.find_one_and_update("users", {"email":data["email"]}, "sessionIds", account["sessionIds"]) != None:
          return(JsonResponse({"errorCode":0, "errorMessage":"Success", "sessionId":sessionId}))
        
      return(JsonResponse(error))
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def signup(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      isValid, error = validateSignupData(data["email"], data["username"], data["password"], data["rePassword"])
      
      if isValid:
        dataAccount = {}
        dataAccount["email"] = data["email"]
        dataAccount["username"] = data["username"]
        dataAccount["salt"] = swiftcrypt.Salts().generate_salt(ConfigObj.salt_length)
        dataAccount["passwordHash"] = swiftcrypt.Hash().hash_password(data["password"], dataAccount["salt"], "sha256")
        dataAccount["sessionIds"] = []
        
        if db.insert_one("users", dataAccount) != None:
          dataPasswords = {"email":dataAccount["email"], "passwords":[], "passwordIndex":-1}
          db.insert_one("users-data", dataPasswords)
          return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
        
      return(JsonResponse(error))
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form", "data":data}))
    
def vaultGet(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      account = db.find_one("users", {"email":data["email"]})

      if account != None:
        if validateSession(account, data):
          dataPasswords = db.find_one("users-data", {"email":account["email"]})
          for value in dataPasswords["passwords"]:
            passwordDecrypt = encryptor.decryptor(account["salt"], account["passwordHash"], value["password"])
            value["password"] = passwordDecrypt

          return(JsonResponse({"errorCode":0, "errorMessage":"Success", "passwords":dataPasswords["passwords"]}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
    
    except Exception as e:
      print("exception")
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))
    
def vaultNew(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      account = db.find_one("users", {"email":data["email"]})
      
      if account != None:
        if validateSession(account, data):
          passwordEncrypt = encryptor.encrypt(account["salt"], data["password"], account["passwordHash"])

          dataPasswords = db.find_one("users-data", {"email":account["email"]})
          try:
            url = data["url"]
          except:
            data["url"] = ""
          dataPasswords["passwordIndex"] += 1
          dataPasswords["passwords"].append({"name":data["name"], "username":data["username"], "password":passwordEncrypt, "url":data["url"], "id":dataPasswords["passwordIndex"]})
            
          if db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"]) != None:
            db.find_one_and_update("users-data", {"email":account["email"]}, "passwordIndex", dataPasswords["passwordIndex"])
            return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))

        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def vaultEdit(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      account = db.find_one("users", {"email":data["email"]})
      
      if account != None:
        if validateSession(account, data):
          dataPasswords = db.find_one("users-data", {"email":account["email"]})
          for entry in dataPasswords["passwords"]:
            if entry["id"] == data["id"]:
              newPasswordEncrypt = encryptor.encrypt(account["salt"], data["newPassword"], account["passwordHash"])
              entry["password"] = newPasswordEncrypt
              entry["name"] = data["newName"]
              entry["username"] = data["newUsername"]
              entry["url"] = data["newUrl"]
              if db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"]) != None:
                return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
              
              return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"No Entry exists with that ID"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))

    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def vaultDelete(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      account = db.find_one("users", {"email":data["email"]})

      if account != None:
        if validateSession(account, data):
          dataPasswords = db.find_one("users-data", {"email":account["email"]})
          for entry in dataPasswords["passwords"]:
            if entry["name"] == data["name"]:
              dataPasswords["passwords"].remove(entry)

              if db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"]) != None:
                return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))

              return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"No Entry with that name"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def sessionGet(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      account = db.find_one("users", {"email":data["email"]})

      if account != None:
        if validateSession(account, data):
          return(JsonResponse({"errorCode":0, "errorMessage":"Success", "sessionIds":account["sessionIds"]}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
    
    except Exception as e:
      print("exception")
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def sessionEdit(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      account = db.find_one("users", {"email":data["email"]})
      
      if account != None:
        if validateSession(account, data):
          for entry in account["sessionIds"]:
            if entry["sessionId"] == data["sessionIdW"]:
              entry["name"] = data["newName"]
              if db.find_one_and_update("users", {"email":account["email"]}, "sessionIds", account["sessionIds"]) != None:
                return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
              
              return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"No Entry exists with that Name"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))

    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def sessionDelete(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      account = db.find_one("users", {"email":data["email"]})

      if account != None:
        if validateSession(account, data):
          for entry in account["sessionIds"]:
            if entry["sessionId"] == data["sessionIdW"]:
              account["sessionIds"].remove(entry)

              if db.find_one_and_update("users", {"email":account["email"]}, "sessionIds", account["sessionIds"]) != None:
                return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))

              return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"No Entry with that name"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def home(request):
  return(render(request, "home/index.html", {'title':'APM - Home'}))

def docs(request):
  return(render(request, "docs/index.html", {'title':'APM - Docs'}))