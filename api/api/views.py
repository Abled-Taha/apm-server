from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import json
from .settings import db, ConfigObj

def validateSignupData(email, username, password, rePassword):
  if db.find_one("users", {"email":email}) == None:
    if len(username) >= ConfigObj.config["username_min_length"] and len(username) <= ConfigObj.config["username_max_length"] and username.isalnum():
      if password == rePassword and len(password) >= ConfigObj.config["password_min_length"] and len(password) <= ConfigObj.config["password_max_length"]:
        return(True, {"errorCode":0, "errorMessage":"Success"})
      return(False, {"errorCode":1, "errorMessage":"Error in Password field"})
    return(False, {"errorCode":1, "errorMessage":"Error in Username field"})
  return(False, {"errorCode":1, "errorMessage":"Error in Email field"})

def signin(request):
  pass

def signup(request):
  if request.method != "POST":
    return(HttpResponse("Method not Allowed."))
  else:
    try:
      data = json.loads(request.body)
      isValid, error = validateSignupData(data["email"], data["username"], data["password"], data["rePassword"])
      if isValid:
        if db.insert_one("users", data) != None:
          return(JsonResponse({"errorCode":0, "errorMessage":"Success"}))
        print("No Collection Found with that Name")
      return(JsonResponse(error))
    except Exception as e:
      print(e)
      return(JsonResponse({"errorCode":1, "errorMessage":"Invalid Form"}))

def docs(request):
  return(render(request, "docs/index.html", {'title':'APM - Docs'}))