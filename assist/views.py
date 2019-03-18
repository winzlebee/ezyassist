from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Respond to a request for the home page
    return HttpResponse("This will be the index for the main assist page.")

def lodge(request):
    pass
