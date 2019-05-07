from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.urls import reverse

from .models import PricingModel, UserProfileModel, AssistanceRequest, AssistanceApproval
from .forms import *

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

    if 'failure' in request.GET:
        context['isFailure'] = True

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
        return HttpResponseRedirect('/assist/dash')
    else:
        return HttpResponseRedirect('/assist?failure=1')

def signup_view(request):
    
    signup_template = loader.get_template('signup_view.html')
    pricing_models = PricingModel.objects.order_by('yearlyPrice')

    context = {
        'pricings': pricing_models,
        'pageinfo': {
            'title': "EzyAssist - Signup"
        },
        'hasErrors':False
    }

    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        file_form = DocumentForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile = profile_form.save()
            user.profile.user = user

            if user.profile.isServicer and file_form.is_valid():
                # We checked for this initially.
                document = file_form.save()
                user.profile.optionalDocument = document

            user.profile.save()
            user.save()

            return HttpResponseRedirect('/assist')
        else:
            context['hasErrors'] = True
            context['errors'] = user_form.errors.as_ul()
            context['profileErrors'] = profile_form.errors.as_ul()
            context['fileErrors'] = file_form.errors.as_ul()
    else:
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

    context["user"] = user_form
    context["profile"] = profile_form

    return HttpResponse(signup_template.render(context, request))

@login_required
def withdraw_view(request, withdraw_pk=None):
    withdraw = AssistanceRequest.objects.get(id=withdraw_pk)
    if withdraw.creator == request.user:
        withdraw.delete()
    return HttpResponseRedirect(reverse('dash'))

@login_required
def respond_view(request, respond_pk=None):
    # Use the respond_pk to create an AssistanceResponse for a request for the user
    return HttpResponseRedirect(reverse('dash'))

@login_required
def dash_view(request):
    userInstance = request.user
    profileInstance = UserProfileModel.objects.get(user=userInstance)

    context = {
        'user' : userInstance,
        'requests' : AssistanceRequest.objects.filter(creator=userInstance),
        'dist_form' : DistanceSelectForm(),
    }

    if request.method == 'POST':
        distance_form = DistanceSelectForm(request.POST)
        if (distance_form.is_valid()):
            context['dist_form'] = distance_form

    if profileInstance.isServicer:
        return HttpResponse(loader.get_template('servicer_dash_view.html').render(context, request))
    else:
        return HttpResponse(loader.get_template('dash_view.html').render(context, request))

@login_required
def profile_view(request):
    template = loader.get_template('profile_view.html')
    userInstance = UserProfileModel.objects.get(user=request.user)

    context = {
        'form':ProfileForm(instance=userInstance),
        'userProfile':userInstance,
        'hasErrors':False,
        'pricings' : PricingModel.objects.order_by('yearlyPrice'),
    }

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=userInstance)
        if profile_form.is_valid():
            profile = profile_form.save()
            return HttpResponseRedirect('/assist/dash')
        else:
            context['hasErrors'] = True

    return HttpResponse(template.render(context, request))

@login_required
def lodge(request):
    template = loader.get_template('lodge_view.html')
    context = {
        'pageinfo': {
            'title': "EzyAssist - Lodge",
        },
        'user': request.user,
        'userProfile': UserProfileModel.objects.get(user=request.user),
    }

    if request.method == 'POST':
        assistance_form = AssistanceRequestForm(request.POST)
        if assistance_form.is_valid():
            assistanceRequest = assistance_form.save()
            assistanceRequest.creator = request.user
            assistanceRequest.save()
            
            return HttpResponseRedirect('/assist/dash')
        else:
            context['hasErrors'] = True
            context['errors'] = assistance_form.errors.as_ul()

    return HttpResponse(template.render(context, request))

def TandC(request):
    # Respond to a request for the home page
    termsConditions = loader.get_template('terms and conditions.html')
    context = {
	}
    return HttpResponse(termsConditions.render(context, request))