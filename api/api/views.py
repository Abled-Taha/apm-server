from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import functions as func

def index(request):
  return render(request, 'index.html', context={})
