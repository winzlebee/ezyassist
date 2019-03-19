from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    # Respond to a request for the home page
    indexTemplate = loader.get_template('index.html')
    return HttpResponse(indexTemplate.render())

def lodge(request):
    template = loader.get_template('lodge_view.html')
    return HttpResponse(template.render())
