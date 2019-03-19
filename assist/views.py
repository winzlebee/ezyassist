from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import PricingModel

def index(request):
    # Respond to a request for the home page
    pricing_models = PricingModel.objects.order_by('yearlyPrice')
    indexTemplate = loader.get_template('index.html')

    context = {
        'models': pricing_models,
        'pageinfo': {
            'title': "EzyAssist"
        }
    }

    return HttpResponse(indexTemplate.render(context, request))

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/assist')

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/assist/lodge')
    else:
        return HttpResponseRedirect('/')
    
def signup_view(request):
    signup_template = loader.get_template('signup_view.html')
    pricing_models = PricingModel.objects.order_by('yearlyPrice')

    context = {
        'pricings': pricing_models,
        'pageinfo': {
            'title': "EzyAssist - Signup"
        }
    }

    return HttpResponse(signup_template.render(context, request))

@login_required
def lodge(request):
    template = loader.get_template('lodge_view.html')
    context = {
        'pageinfo': {
            'title': "EzyAssist - Lodge"
        }
    }
    return HttpResponse(template.render(context, request))
