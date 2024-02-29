from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import json
import swiftcrypt
import secrets
import string
from .settings import db, ConfigObj

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
      return(False, {"errorCode":1, "errorMessage":"Error in Password field"})
    return(False, {"errorCode":1, "errorMessage":"Error in Username field"})
  return(False, {"errorCode":1, "errorMessage":"Error in Email field"})





def home(request):
  return(render(request, "home/index.html", {'title':'APM - Home'}))

def signin(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  else:
    try:
      data = json.loads(request.body)
      isValid, error, account = validateSigninData(data["email"], data["password"])
      
      if isValid:
        sessionId = generateSessionId()
        account["sessionIds"].append({"name":"", "sessionId":sessionId})
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
        dataAccount = data
        dataAccount["salt"] = swiftcrypt.Salts().generate_salt(ConfigObj.salt_length)
        dataAccount["passwordHash"] = swiftcrypt.Hash().hash_password(dataAccount["password"], dataAccount["salt"], "sha256")
        dataAccount["sessionIds"] = []
        del dataAccount["rePassword"]; del dataAccount["password"]
        
        if db.insert_one("users", dataAccount) != None:
          return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
        
      return(JsonResponse(error))
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def docs(request):
  return(render(request, "docs/index.html", {'title':'APM - Docs'}))