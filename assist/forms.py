from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfileModel, Document, AssistanceRequest, AssistanceReview, AssistanceApproval

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class LeaveReviewForm(forms.ModelForm):
    class Meta:
        model = AssistanceReview
        fields = ('star_rating', 'text_rating')

class CreateApprovalForm(forms.ModelForm):
    class Meta:
        model = AssistanceApproval
        fields = ('quote',)

class AssistanceRequestForm(forms.ModelForm):
    class Meta:
        model = AssistanceRequest
        fields = ('latitude', 'longitude', 'request_details')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ('address', 'registration', 'isServicer', 'subscription')

class DistanceSelectForm(forms.Form):
    distance = forms.ChoiceField(widget=forms.Select(attrs={"class" : "custom-select custom-select-sm"}), choices=(('20', '20km'), ('50', '50km'), ('100', '100km')), label='')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)