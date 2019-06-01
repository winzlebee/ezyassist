from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

import requests
import json
from assist.utils import haversine

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
        return HttpResponseRedirect(reverse('dash'))
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

# Finalize an assistance request, adding it to the past assistance requests database and allowing a rating to be left.
@login_required
def finalize_request(request, request_pk=None):
    finalize_template = loader.get_template("finalize_view.html")
    toFinalize = AssistanceRequest.objects.get(id=request_pk)

    context = {
        'requestItem' : toFinalize
    }

    if request.method == 'POST':
        user_form = LeaveReviewForm(request.POST)

        if user_form.is_valid():
            fin_model = user_form.save()
            fin_model.creator = request.user
            fin_model.target = AssistanceApproval.objects.get(request=toFinalize).repairer
            fin_model.save()

            toFinalize.is_finalized = True
            toFinalize.save()

        # Create the review object and spit the user back to the dash
        return HttpResponseRedirect(reverse('dash'))
    else:
        return HttpResponse(finalize_template.render(context, request))

@login_required
def approve_response(request, approval_pk=None):
    # Respond to the request by setting its flag to true
    response_toApprove = AssistanceApproval.objects.get(id=approval_pk)
    response_toApprove.is_approved = True
    response_toApprove.save()

    return HttpResponseRedirect(reverse('dash'))

@login_required
def view_responses(request, request_pk=None):
    # Get the relevant response and check it belongs to the user
    curr_request = AssistanceRequest.objects.get(id=request_pk)
    request_array = []

    assistance_approvals = AssistanceApproval.objects.filter(request=request_pk)

    for service_request in assistance_approvals:
        relevant_reviews = AssistanceReview.objects.filter(target=service_request.repairer)
        request_array.append((service_request, round(relevant_reviews.aggregate(Avg('star_rating'))['star_rating__avg'], 2), relevant_reviews.count()))

    view_responses_template = loader.get_template("responses_view.html")
    context = {
        "responses" : request_array
    }
    return HttpResponse(view_responses_template.render(context, request))

@login_required
def remove_response(request, approval_pk=None):
    # Removing a response deletes it on the admin and user side
    curr_response = AssistanceApproval.objects.get(id=approval_pk)
    curr_response.delete()

    return HttpResponseRedirect(reverse('dash'))

@login_required
def ratings_view(request, profile_id=None):
    # Find all ratings related to this professional
    ratings_user = User.objects.get(id=profile_id)
    ratings = getRatingsArray(ratings_user)

    ratings_template = loader.get_template("ratings_view.html")

    return HttpResponse(ratings_template.render({"user": ratings_user, "ratings": ratings}, request))


@login_required
def respond_view(request, respond_pk=None):
    # Use the respond_pk to create an AssistanceResponse for a request for the user
    relevantRequest = AssistanceRequest.objects.get(id=respond_pk);

    context = {"request" : relevantRequest }

    if request.method == "POST":
        # Check the service request came from the specified user
        response_form = CreateApprovalForm(request.POST)

        if response_form.is_valid():
            assistanceResponse = response_form.save()

            assistanceResponse.repairer = request.user
            assistanceResponse.request = relevantRequest
            assistanceResponse.save()

            return HttpResponseRedirect(reverse('dash'))
        else:
            context['errors'] = True

    # Otherwise, we display the form related to responding to requests
    response_template = loader.get_template("respond_view.html")

    return HttpResponse(response_template.render(context, request))

@login_required
def reports_view(request):
    user_model = UserProfileModel.objects.get(user=request.user)
    reports_template = loader.get_template("generate_reports_view.html")

    return HttpResponse(reports_template.render({"isServicer" : user_model.isServicer}, request))

@login_required
def service_report_view(request):
    user_profile = UserProfileModel.objects.get(user=request.user)
    template = loader.get_template("service_report_view.html")

    service_entries = []
    if user_profile.isServicer:
        relevant_reports = AssistanceApproval.objects.filter(repairer=request.user, is_approved=True)
        for report in relevant_reports:
            if report.request.is_finalized:
                service_entries.append((report.request.lodge_time, report.quote, report.request.request_details))
    else:
        relevant_requests = AssistanceRequest.objects.filter(creator=request.user, is_finalized=True)
        for ass_request in relevant_requests:
            r_approval = AssistanceApproval.objects.get(request=ass_request)
            service_entries.append((ass_request.lodge_time, r_approval.quote, ass_request.request_details))

    service_entries = sorted(service_entries, key=lambda req: req[0], reverse=True)

    return HttpResponse(template.render({'entries' : service_entries}, request))

@login_required
def withdraw_response_view(request, request_pk=None):
    # Withdraw an AssistanceApproval
    ass_request = AssistanceRequest.objects.get(id=request_pk)
    approvals = AssistanceApproval.objects.filter(request=ass_request, repairer=request.user)

    # If the response belongs to the user, remove it
    if approvals.count() > 0:
        approvals[0].delete()

    return HttpResponseRedirect(reverse('dash'))

@login_required
def dash_view(request):
    userInstance = request.user
    profileInstance = UserProfileModel.objects.get(user=userInstance)

    # Default distance when visiting the page
    targetDistance = 20

    context = {
        'user' : userInstance,
        'dist_form' : DistanceSelectForm(initial={'distance' : targetDistance}),
    }

    if request.method == 'POST':
        distance_form = DistanceSelectForm(request.POST)
        if (distance_form.is_valid()):
            targetDistance = float(distance_form.cleaned_data['distance'])
            context['dist_form'] = distance_form

    if profileInstance.isServicer:
        
        success_flag = False

        # Use the requests library to make a request to get the latitude and longitude
        try:
            response = requests.get('https://api.opencagedata.com/geocode/v1/json?q='+ profileInstance.address + '&key=9b31b6d3f4264926b4440dbd81ea80c6', timeout=10.0)
            success_flag = True
        except requests.ReadTimeout:
            success_flag = False

        # Response is in JSON - parse to get the address
        if success_flag:
            if response.status_code == 200:
                json_object = json.loads(response.content)
                s_latitude = float(json_object['results'][0]['geometry']['lat'])
                s_longitude = float(json_object['results'][0]['geometry']['lng'])
                success_flag = True

        matchingRequests = []

        for r in AssistanceRequest.objects.all():
            if success_flag:
                dist = haversine(s_latitude, s_longitude, r.latitude, r.longitude)
                if dist < targetDistance and not r.isFinalized():
                    matchingRequests.append((r, round(dist, 2), r.isRespondedBy(request.user)))
            elif not r.isFinalized():
                # Handle the case where we don't get the data
                matchingRequests.append((r, 0, r.isRespondedBy(request.user)))


        context['requests'] = sorted(matchingRequests, key=lambda req: req[1])
        return HttpResponse(loader.get_template('servicer_dash_view.html').render(context, request))
    else:
        context['requests'] = AssistanceRequest.objects.filter(creator=userInstance, is_finalized=False)
        return HttpResponse(loader.get_template('dash_view.html').render(context, request))

def getRatingsArray(user):
    assistance_reviews = AssistanceReview.objects.filter(target=user)

    ass_array = []
    for review in assistance_reviews:
        ass_array.append((review, range(0, review.star_rating)))

    return ass_array

@login_required
def profile_view(request):
    template = loader.get_template('profile_view.html')
    userInstance = UserProfileModel.objects.get(user=request.user)

    context = {
        'form':ProfileForm(instance=userInstance),
        'userProfile':userInstance,
        'hasErrors':False,
        'pricings' : PricingModel.objects.order_by('yearlyPrice'),
        'reviews' : getRatingsArray(request.user),
    }

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=userInstance)
        if profile_form.is_valid():
            profile = profile_form.save()
            profile.isServicer = userInstance.isServicer
            profile.save()
            return HttpResponseRedirect(reverse('dash'))
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