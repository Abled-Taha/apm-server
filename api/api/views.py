from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
import swiftcrypt, base64, datetime
from .settings import db, ConfigObj, ImageHandlerObj, LogHandlerObj, EmailHandlerObj, functions

def signin(request):
      success, data, error = functions.runCommonChecks(request, "Signin")
      if success:
        error, account = functions.validateSigninData(data["email"], data["password"])
        if error["errorCode"] == 0:
          # Generate Session ID
          sessionId = functions.generateSessionId()
          # Set Default Values
          if data.get("sessionName") == None:
            data["sessionName"] = ""
          # Add Session ID to List
          account["sessionIds"].append({"name":data["sessionName"], "sessionId":sessionId})
          # Remove Oldest Session
          if len(account["sessionIds"]) > ConfigObj.max_sessions:
            del account["sessionIds"][0]
          # Update Database
          db.find_one_and_update("users", {"email":data["email"]}, "sessionIds", account["sessionIds"])

          LogHandlerObj.write("Signin", "OK", data, data["email"])
          return(JsonResponse({"errorCode":0, "errorMessage":"Success", "sessionId":sessionId, "salt":account["salt"], "username":account["username"]}))
          
        LogHandlerObj.write("Signin", "FAILED", data, data["email"], error["errorMessage"])
        return(JsonResponse(error))
      else:
        LogHandlerObj.write("Signin", "FAILED", data, "N/A", error["errorMessage"])
        return(JsonResponse(error))
      
def signup(request):
  success, data, error = functions.runCommonChecks(request, "Signup")
  if success:
    error = functions.validateSignupData(data["email"], data["username"], data["password"], data["rePassword"])
          
    if error["errorCode"] == 0:
      dataAccount = {
        "email":data["email"],
        "username":data["username"],
        "salt":swiftcrypt.Salts().generate_salt(ConfigObj.salt_length),
        "passwordHash":"",
        "masterPasswordHistory":[],
        "sessionIds":[],
        "otps":[]
      }
      dataAccount["passwordHash"] = swiftcrypt.Hash().hash_password(data["password"], dataAccount["salt"], "sha256")
      dataAccount["masterPasswordHistory"].append(dataAccount["passwordHash"])
      if ConfigObj.email_verification == True:
        dataAccount["verified"] = False
      else:
        dataAccount["verified"] = True
            
      dataPasswords = {"email":dataAccount["email"], "passwords":[], "passwordIndex":-1}
      
      db.insert_one("users", dataAccount)
      db.insert_one("users-data", dataPasswords)

      LogHandlerObj.write("Signup", "OK", data, data["email"])
      return(JsonResponse(error))
    LogHandlerObj.write("Signup", "FAILED", data, data["email"], error["errorMessage"])
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))
    
def vaultGet(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Vault-Get")
  if success:
    dataPasswords = db.find_one("users-data", {"email":account["email"]})
    if dataPasswords != None:
      error["passwords"] = dataPasswords["passwords"]
      error["verified"] = account["verified"]
      return(JsonResponse(error))
    error["errorMessage"] = "Error in Database"
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))
    
def vaultNew(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Veult-New")
  if success:
    dataPasswords = db.find_one("users-data", {"email":account["email"]})
    if dataPasswords != None:
      # Add Default Values
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
      if data.get("url") == None:
        data["url"] = ""
      else:
        data["url"] = ("https://" + data["url"].removeprefix("https://"))
      # Update Password Index
      dataPasswords["passwordIndex"] += 1
      dataPasswords["passwords"].append({"name":data["name"], "username":data["username"], "password":data["password"], "url":data["url"], "note":data["note"], "id":dataPasswords["passwordIndex"]})
      # Write to Database
      db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"])
      db.find_one_and_update("users-data", {"email":account["email"]}, "passwordIndex", dataPasswords["passwordIndex"])

      return(JsonResponse(error))
    error["errorMessage"] = "Error in Database"
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))

def vaultEdit(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Vault-Edit")
  if success:
    dataPasswords = db.find_one("users-data", {"email":account["email"]})

    if dataPasswords != None:
      # Add Default Values
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
      if data.get("newUrl") == None:
        data["newUrl"] = ""
      else:
        data["newUrl"] = ("https://" + data["newUrl"].removeprefix("https://"))
      # Find Entry in Database
      for entry in dataPasswords["passwords"]:
        if entry["id"] == data["id"]:
          # Update Entry
          entry["password"] = data["newPassword"]
          entry["name"] = data["newName"]
          entry["username"] = data["newUsername"]
          entry["url"] = data["newUrl"]
          entry["note"] = data["newNote"]
          # Write to Database
          db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"])

          return(JsonResponse(error))
      error["errorMessage"] = "No Entry exists with that ID"
      return(JsonResponse(error))
    error["errorMessage"] = "Error in Database"
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))

def vaultDelete(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Vault-Delete")
  if success:
    dataPasswords = db.find_one("users-data", {"email":account["email"]})
    if dataPasswords != None:
      # Find Entry in Database
      for entry in dataPasswords["passwords"]:
        if entry["id"] == data["id"]:
          # Remove Entry
          dataPasswords["passwords"].remove(entry)
          # Write to Database
          db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", dataPasswords["passwords"])

          return(JsonResponse(error))
      error["errorMessage"] = "No Entry exists with that ID"
      return(JsonResponse(error))
    error["errorMessage"] = "Error in Database"
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))

def sessionGet(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Session-Get")
  if success:
    error["sessionIds"] = account["sessionIds"]
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))

def sessionEdit(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Session-Edit")
  if success:
    # Find Entry in Database
    for entry in account["sessionIds"]:
      if entry["sessionId"] == data["sessionIdW"]:
        # Update Entry
        entry["name"] = data["newName"]
        # Write to Database
        db.find_one_and_update("users", {"email":account["email"]}, "sessionIds", account["sessionIds"])

        return(JsonResponse(error))
    error["errorMessage"] = "No Entry exists with that Name"
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))

def sessionDelete(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Session-Delete")
  if success:
    # Find Entry in Database
    for entry in account["sessionIds"]:
      if entry["sessionId"] == data["sessionIdW"]:
        # Remove Entry
        account["sessionIds"].remove(entry)
        # Write to Database
        db.find_one_and_update("users", {"email":account["email"]}, "sessionIds", account["sessionIds"])

        return(JsonResponse(error))
    error["errorMessage"] = "No Entry exists with that Name"
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))
    
def ppGet(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "PP-Get")
  if success:
    imagePath = ImageHandlerObj.getImagePath(data["username"])
    imageBytesObj = ImageHandlerObj.getImageBytes(imagePath)
    # Converting bytes object to literal string
    imageBytesStr = repr(imageBytesObj)

    error["pp"] = imageBytesStr
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))
    
def ppNew(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "PP-New")
  if success:
    imageBytesObj = base64.b64decode(data["image"].removeprefix("b'").removesuffix("'").encode())
    ImageHandlerObj.writeBytesObjToImage(data["username"], imageBytesObj)
    return(JsonResponse(error))
  else:
    return(JsonResponse(error))

def vaultImport(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Vault-Import")
  if success:
    passwordIndex = accountData["passwordIndex"]
    # Change the ID of each entry
    for entry in data["items"]:
      entry["id"] = passwordIndex + 1
      passwordIndex += 1
    # Add new entries
    passwords = accountData["passwords"] + data["items"]
    # Write to Database
    db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", passwords)
    db.find_one_and_update("users-data", {"email":account["email"]}, "passwordIndex", passwordIndex)

    return(JsonResponse(error))
  else:
    return(JsonResponse(error))

def otpSend(request):
  if ConfigObj.email_verification == True:
    success, data, account, accountData, error = functions.runAllChecks(request, "OTP-Send")
    if success:
      # Generate OTP
      otp = functions.generateOtp()
      # Generate OTP Data
      otpData = {
        "otp": otp,
        "expiry": (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime("%Y-%m-%d_%H:%M:%S"),
        "purpose": "Email Verification"
      }
      # Send Email
      EmailHandlerObj.send(data["email"], "APM - Email Verification", f"Your Verification Code is: {otp}")
      # Add OTP to Database
      otps = account["otps"]
      otps.append(otpData)
      db.find_one_and_update("users", {"email": data["email"]}, "otps", otps)

      return(JsonResponse(error))
    else:
      return(JsonResponse(error))
  else:
    return(JsonResponse({"errorCode":1, "errorMessage":"Email Verification is Disabled"}))
    
def otpVerify(request):
  if ConfigObj.email_verification == True:
    success, data, account, accountData, error = functions.runAllChecks(request, "OTP-Verify")
    if success:
      if functions.validateOtp(account, data["otp"]):
        return(JsonResponse(error))
      error["errorMessage"] = "Invalid OTP"
      return(JsonResponse(error))
    else:
      return(JsonResponse(error))
  else:
    return(JsonResponse({"errorCode":1, "errorMessage":"Email Verification is Disabled"}))

def changePassword(request):
  success, data, account, accountData, error = functions.runAllChecks(request, "Change-Password")
  if success:
    # Verify Master Password
    if swiftcrypt.Checker().verify_password(data["oldPassword"], account["passwordHash"], account["salt"], "sha256"):
      # Hash New Password
      account["passwordHash"] = swiftcrypt.Hash().hash_password(data["newPassword"], account["salt"], "sha256")
      # Add New Password To Password History
      account["masterPasswordHistory"].append(account["passwordHash"])
      # Update Password
      db.find_one_and_update("users", {"email":account["email"]}, "passwordHash", account["passwordHash"])
      db.find_one_and_update("users", {"email":account["email"]}, "masterPasswordHistory", account["masterPasswordHistory"])

      # Update Vault Passwords
      for newEntry in data["passwords"]:
        for entry in accountData["passwords"]:
          if entry["id"] == newEntry["id"]:
            entry["password"] = newEntry["password"]
            entry["note"] = newEntry["note"]
            break
      # Write to Database
      db.find_one_and_update("users-data", {"email":account["email"]}, "passwords", accountData["passwords"])

      return(JsonResponse(error))
    return({"errorCode":1, "errorMessage":"Incorrect Password"}, account)

  else:
    return(JsonResponse(error))

def home(request):
  return(render(request, "home/index.html", {'title':'APM - Home'}))

def docs(request):
  if ConfigObj.docs_enabled:
    return(render(request, "docs/index.html", {'title':'APM - Docs'}))
  else:
    return(HttpResponse("DOCS DISABLED."))