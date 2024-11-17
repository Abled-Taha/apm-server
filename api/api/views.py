from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import json, swiftcrypt, base64, datetime
from .settings import db, ConfigObj, ImageHandlerObj, LogHandlerObj, EmailHandlerObj
from .Functions import Functions

functions = Functions(db, ConfigObj)

def signin(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        isValid, error, account = functions.validateSigninData(data["email"], data["password"])
        
        if isValid:
          sessionId = functions.generateSessionId()
          try:
            sessionName = data["sessionName"]
          except:
            sessionName = ""
          account["sessionIds"].append({"name":sessionName, "sessionId":sessionId})
          if len(account["sessionIds"]) > ConfigObj.max_sessions:
            del account["sessionIds"][0]

          if db.find_one_and_update("users", {"email":data["email"]}, "sessionIds", account["sessionIds"]) != None:
            LogHandlerObj.write(f"Signin | OK | {data['email']}", data)
            return(JsonResponse({"errorCode":0, "errorMessage":"Success", "sessionId":sessionId, "salt":account["salt"], "username":account["username"]}))
          
        LogHandlerObj.write(f"Signin | FAILED | {data['email']} | {error["errorMessage"]}", data)
        return(JsonResponse(error))
      LogHandlerObj.write(f"Signin | FAILED | {data['email']} | Invalid Api Token", data)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
    except Exception as e:
      print(e)
      LogHandlerObj.write(f"Signin | FAILED | {data['email']} | Invalid Form", data)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def signup(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        isValid, error = functions.validateSignupData(data["email"], data["username"], data["password"], data["rePassword"])
        
        if isValid:
          dataAccount = {}
          dataAccount["email"] = data["email"]
          dataAccount["username"] = data["username"]
          dataAccount["salt"] = swiftcrypt.Salts().generate_salt(ConfigObj.salt_length)
          dataAccount["passwordHash"] = swiftcrypt.Hash().hash_password(data["password"], dataAccount["salt"], "sha256")
          dataAccount["sessionIds"] = []
          dataAccount["otps"] = []
          if ConfigObj.email_verification == True:
            dataAccount["verified"] = False
          else:
            dataAccount["verified"] = True
          
          if db.insert_one("users", dataAccount) != None:
            dataPasswords = {"email":dataAccount["email"], "passwords":[], "passwordIndex":-1}
            db.insert_one("users-data", dataPasswords)
            LogHandlerObj.write(f"Signup | OK | {data['email']}", data)
            return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
          
        LogHandlerObj.write(f"Signup | FAILED | {data['email']} | {error["errorMessage"]}", data)
        return(JsonResponse(error))
      LogHandlerObj.write(f"Signup | FAILED | {data['email']} | Invalid Api Token", data)
      return (JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
    except Exception as e:
      print(e)
      LogHandlerObj.write(f"Signup | FAILED | {data['email']} | Invalid Form", data)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form", "data":data}))
    
def vaultGet(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})

        if account != None:
          if functions.validateSession(account, data):
            dataPasswords = db.find_one("users-data", {"email":account["email"]})
            if dataPasswords != None:
              return(JsonResponse({"errorCode":0, "errorMessage":"Success", "passwords":dataPasswords["passwords"], "verified":account["verified"]}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
    
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
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})
        
        if account != None:
          if functions.validateSession(account, data):
            dataPasswords = db.find_one("users-data", {"email":account["email"]})
            if dataPasswords != None:
              if data.get("name") == None:
                data["name"] = ""
              if data.get("username") == None:
                data["username"] = ""
              if data.get("password") == None:
                data["password"] = ""
              if data.get("url") == None:
                data["url"] = ""
              if data.get("note") == None:
                data["note"] = ""
                
              data["url"] = data["url"].removeprefix("https://")
              data["url"] = "https://" + data["url"]

              dataPasswords["passwordIndex"] += 1
              dataPasswords["passwords"].append({"name":data["name"], "username":data["username"], "password":data["password"], "url":data["url"], "note":data["note"], "id":dataPasswords["passwordIndex"]})
                
              if db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"]) != None:
                db.find_one_and_update("users-data", {"email":account["email"]}, "passwordIndex", dataPasswords["passwordIndex"])
                return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
              return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))

          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def vaultEdit(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})
        
        if account != None:
          if functions.validateSession(account, data):
            dataPasswords = db.find_one("users-data", {"email":account["email"]})

            if dataPasswords != None:
              if data.get("newName") == None:
                data["newName"] = ""
              if data.get("newUsername") == None:
                data["newUsername"] = ""
              if data.get("newPassword") == None:
                data["newPassword"] = ""
              if data.get("newUrl") == None:
                data["newUrl"] = ""
              if data.get("newNote") == None:
                data["newNote"] = ""
                
              data["newUrl"] = data["newUrl"].removeprefix("https://")
              data["newUrl"] = "https://" + data["newUrl"]

              for entry in dataPasswords["passwords"]:
                if entry["id"] == data["id"]:
                  entry["password"] = data["newPassword"]
                  entry["name"] = data["newName"]
                  entry["username"] = data["newUsername"]
                  entry["url"] = data["newUrl"]
                  entry["note"] = data["newNote"]
                  if db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"]) != None:
                    return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
                  
                  return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
              return(JsonResponse({"errorCode":1, "errorMessage":"No Entry exists with that ID"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))

    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def vaultDelete(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})

        if account != None:
          if functions.validateSession(account, data):
            dataPasswords = db.find_one("users-data", {"email":account["email"]})

            if dataPasswords != None:
              for entry in dataPasswords["passwords"]:
                if entry["id"] == data["id"]:
                  dataPasswords["passwords"].remove(entry)

                  if db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"]) != None:
                    return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))

                  return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
              return(JsonResponse({"errorCode":1, "errorMessage":"No Entry with that name"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def sessionGet(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))

  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})

        if account != None:
          if functions.validateSession(account, data):
            return(JsonResponse({"errorCode":0, "errorMessage":"Success", "sessionIds":account["sessionIds"]}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
    
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
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})
        
        if account != None:
          if functions.validateSession(account, data):
            for entry in account["sessionIds"]:
              if entry["sessionId"] == data["sessionIdW"]:
                entry["name"] = data["newName"]
                if db.find_one_and_update("users", {"email":account["email"]}, "sessionIds", account["sessionIds"]) != None:
                  return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
                
                return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"No Entry exists with that Name"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))

    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def sessionDelete(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})

        if account != None:
          if functions.validateSession(account, data):
            for entry in account["sessionIds"]:
              if entry["sessionId"] == data["sessionIdW"]:
                account["sessionIds"].remove(entry)

                if db.find_one_and_update("users", {"email":account["email"]}, "sessionIds", account["sessionIds"]) != None:
                  LogHandlerObj.write(f"Logout | OK | {data['email']}", data)
                  return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))

                LogHandlerObj.write(f"SessionDelete | FAILED | {data['email']} | Error in Database", data)
                return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
            LogHandlerObj.write(f"SessionDelete | FAILED | {data['email']} | No Entry with that name", data)
            return(JsonResponse({"errorCode":1, "errorMessage":"No Entry with that name"}))
          LogHandlerObj.write(f"SessionDelete | FAILED | {data['email']} | Invalid Session Id", data)
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        LogHandlerObj.write(f"SessionDelete | FAILED | {data['email']} | No Account exists with that Email", data)
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))
    
def ppGet(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})

        if account != None:
          if functions.validateSession(account, data):
            imagePath = ImageHandlerObj.getImagePath(data["username"])
            with open(imagePath, "rb") as image_file:
              image64 = base64.standard_b64encode(image_file.read())
              image64 = f"{image64}"
            return(JsonResponse({"errorCode":0, "errorMessage":"Success", "pp":image64}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))
    
def ppNew(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})

        if account != None:
          if functions.validateSession(account, data):
            image = base64.b64decode(data["image"].removeprefix("b'").removesuffix("'").encode())

            success = ImageHandlerObj.updatedImage(data["username"], image)
            if success:
              return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Internal Error"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def vaultImport(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  
  else:
    try:
      data = json.loads(request.body)
      if functions.validateApiToken(data.get("apiToken")):
        account = db.find_one("users", {"email":data["email"]})

        if account != None:
          accountData = db.find_one("users-data", {"email":account["email"]})
          
          if accountData != None:
            if functions.validateSession(account, data):
              passwordIndex = accountData["passwordIndex"]
              for entry in data["items"]:
                entry["id"] = passwordIndex + 1
                passwordIndex += 1

              passwords = accountData["passwords"] + data["items"]
              if db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", passwords) != None:
                if db.find_one_and_update("users-data", {"email":account["email"]}, "passwordIndex", passwordIndex) != None:
                  return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
              return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
      
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def otpSend(request):
  if ConfigObj.email_verification == True:
    if request.method != "POST":
      return(HttpResponse("Method not Allowed."))
    
    else:
      try:
        data = json.loads(request.body)
        if functions.validateApiToken(data.get("apiToken")):
          account = db.find_one("users", {"email":data["email"]})

          if account != None:
            if functions.validateSession(account, data):
              otp = functions.generateOtp()
              otpData = {
                "otp": otp,
                "expiry": (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime("%Y-%m-%d_%H:%M:%S"),
                "purpose": "Email Verification"
              }
              if EmailHandlerObj.send(data["email"], "APM - Email Verification", f"Your Verification Code is: {otp}"):
                otps = account["otps"]
                otps.append(otpData)
                db.find_one_and_update("users", {"email": data["email"]}, "otps", otps)
                return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
              return(JsonResponse({"errorCode":1, "errorMessage":"Error in Database"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
        
      except Exception as e:
        print(e)
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))
  else:
    return(JsonResponse({"errorCode":1, "errorMessage":"Email Verification is Disabled"}))
    
def otpVerify(request):
  if ConfigObj.email_verification == True:
    if request.method != "POST":
      return(HttpResponse("Method not Allowed."))
    
    else:
      try:
        data = json.loads(request.body)
        if functions.validateApiToken(data.get("apiToken")):
          account = db.find_one("users", {"email":data["email"]})

          if account != None:
            if functions.validateSession(account, data):
              if functions.validateOtp(account, data["email"], data["otp"]):
                db.find_one_and_update("users", {"email":data["email"]}, "verified", True)
                return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
              return(JsonResponse({"errorCode":1, "errorMessage":"Invalid OTP"}))
            return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Session Id"}))
          return(JsonResponse({"errorCode":1, "errorMessage":"No Account exists with that Email"}))
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Api Token"}))
        
      except Exception as e:
        print(e)
        return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))
  else:
    return(JsonResponse({"errorCode":1, "errorMessage":"Email Verification is Disabled"}))

def home(request):
  return(render(request, "home/index.html", {'title':'APM - Home'}))

def docs(request):
  return(render(request, "docs/index.html", {'title':'APM - Docs'}))