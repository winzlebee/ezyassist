from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import PricingModel
from .models import UserProfileModel
from .forms import SignUpForm
from .forms import ProfileForm

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
        return HttpResponseRedirect('/assist/lodge')
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
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile = profile_form.save()
            user.profile.user = user

            user.profile.save()
            user.save()

            return HttpResponseRedirect('/assist')
        else:
            context['hasErrors'] = True
            context['errors'] = user_form.errors.as_ul()
            context['profileErrors'] = profile_form.errors.as_ul()

    return HttpResponse(signup_template.render(context, request))

@login_required
def profile_view(request):
    template = loader.get_template('profile_view.html')
    userInstance = UserProfileModel.objects.get(user=request.user)

    context = {
        'form':ProfileForm(instance=userInstance),
        'hasErrors':False
    }

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=userInstance)
        if profile_form.is_valid():
            profile = profile_form.save()
            return HttpResponseRedirect('/assist/lodge')
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
    return HttpResponse(template.render(context, request))
