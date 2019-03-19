from django.contrib import admin

from .models import AssistanceRequest
from .models import PricingModel

# Register your models here.
admin.site.register(AssistanceRequest)
admin.site.register(PricingModel)