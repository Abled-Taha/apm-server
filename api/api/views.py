from django.shortcuts import render

def signin(request):
  pass

def signup(request):
  pass

def docs(request):
  return(render(request, "docs/index.html", {'title':'APM - Docs'}))