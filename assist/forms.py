from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfileModel, Document, AssistanceRequest

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class AssistanceRequestForm(forms.ModelForm):
    class Meta:
        model = AssistanceRequest
        fields = ('latitude', 'longitude', 'request_details')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ('address', 'registration', 'isServicer', 'subscription')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)