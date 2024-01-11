from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import functions as func
from . import forms

def index(request):
  return render(request, 'index.html', context={})

def signup(request):
  # Checks for the type of Request (GET, POST, other)
  if request.method == "GET":
    form = forms.SignupForm()
    return render(request, 'signup.html', context={'form':form, 'submitted':False})
  
  elif request.method == "POST":
    # Creates the account
    isValid, error = func.createUser(email=request.POST["email"], username=request.POST["username"], password=request.POST["password"], rePassword=request.POST["rePassword"])

    # Checks whether the returned response should be HTML or JSON
    if request.POST["fromGUI"] == "true":
      return(render(request, 'signup.html', context={'submitted':True, 'isValid':isValid, 'error':error}))

    elif request.POST["fromGUI"] == "false":
      return(JsonResponse({'submitted':True, 'isValid':isValid, 'error':error}))

    # If the the 'submitted' variable is null then the returned response is HTML
    else:
      return(HttpResponse("'submitted' variable neither true nor false"))
  
  else:
    return(HttpResponse("Only GET and POST requests are allowed."))