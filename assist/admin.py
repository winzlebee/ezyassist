from django.contrib import admin

from .models import AssistanceRequest, PricingModel, UserProfileModel

# Register your models here.
admin.site.register(AssistanceRequest)
admin.site.register(PricingModel)
admin.site.register(UserProfileModel)