from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import functions as func
from . import forms

def index(request):
  if request.method == "GET":
    if func.supplyGUIResponse:
      return render(request, 'index.html', context={'title':'APM - API | Index'})
    return(HttpResponse("Only POST requests are allowed on this endpoint."))
  
  elif request.method == "POST":
    return JsonResponse({'error':'The API is working fine.'})
  
  else:
    if func.supplyGUIResponse:
      return HttpResponse("Only GET and POST requests are allowed on this endpoint.")
    return HttpResponse("Only POST requests are allowed on this endpoint.")

def docs(request):
  if request.method == "GET":
    return render(request, 'docs.html', context={'title':'APM - API | Docs'})
  
  else:
    return HttpResponse("Only GET requests are allowed on this endpoint.")

def signup(request):
  # Checks for the type of Request (GET, POST, other)
  if request.method == "GET":
    if func.supplyGUIResponse:
      form = forms.SignupForm()
      return render(request, 'signup.html', context={'title':'APM - API | SignUp', 'form':form, 'submitted':False})
    return(HttpResponse("Onlye GET requests are allowed on this endpoint."))
  
  elif request.method == "POST":
    # Creates the account
    isValid, error = func.createUser(email=request.POST["email"], username=request.POST["username"], password=request.POST["password"], rePassword=request.POST["rePassword"])

    # Checks whether the returned response should be HTML or JSON
    if request.POST["fromGUI"] == "true":
      return(render(request, 'signup.html', context={'title':'APM - API | SignUp', 'submitted':True, 'isValid':isValid, 'error':error}))

    elif request.POST["fromGUI"] == "false":
      return(JsonResponse({'submitted':True, 'isValid':isValid, 'error':error}))

    # If the the 'submitted' variable is null then the returned response is HTML
    else:
      return(HttpResponse("'submitted' variable neither true nor false"))
  
  else:
    if func.supplyGUIResponse:
      return(HttpResponse("Only GET and POST requests are allowed on this endpoint."))
    return(HttpResponse("Only GET requests are allowed on this endpoint."))
  
def login(request):
  # Checks for the type of Request (GET, POST, other)
  if request.method == "GET":
    if func.supplyGUIResponse:
      form = forms.LoginForm()
      return render(request, 'login.html', context={'title':'APM - API | Login', 'form':form, 'submitted':False})
    return(HttpResponse("Only GET requests are allowed on this endpoint."))
  
  elif request.method == "POST":
  #   # Creates the account
    isValid, error, account = func.loginUser(request=request, email=request.POST["email"], password=request.POST["password"])
    
  #   if error != "Logged In":
  #     return render(request, 'login.html', context={})
    
    
    # Sets a dummy account variable if the account variable is None
    if account == None:
      account = {'username':''}

    # Checks whether the returned response should be HTML or JSON
    if request.POST["fromGUI"] == "true":
      return(render(request, 'login.html', context={'title':'APM - API | Login', 'submitted':True, 'isValid':isValid, 'error':error, 'username':account["username"]}))

    elif request.POST["fromGUI"] == "false":
      return(JsonResponse({'submitted':True, 'isValid':isValid, 'error':error, 'username':account["username"]}))

    # If the the 'submitted' variable is null then the returned response is HTML
    else:
      return(HttpResponse("'submitted' variable neither true nor false"))
  
  else:
    if func.supplyGUIResponse:
      return(HttpResponse("Only GET and POST requests are allowed on this endpoint."))
    return(HttpResponse("Only GET requests are allowed on this endpoint."))

def vault(request):
  if request.method == "GET":
    return(HttpResponse("Only GET requests are allowed on this endpoint."))
  
  elif request.method == "POST":
    try:
      # isValid, error, account = func.loginUser(request=request, email=request.POST["email"], password=request.POST["password"])
      pass
    except Exception as e:
      return(False, "Form not valid.")

  else:
    return(HttpResponse("Only GET requests are allowed on this endpoint."))