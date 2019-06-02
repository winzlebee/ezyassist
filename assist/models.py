from django.conf import settings
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# All the models that are required for the maintenance booking engine are defined here.
# For those not familiar with Django, all data sets are assosciated with models

# A request made for assistance
class AssistanceRequest(models.Model):
    
    # We cascade so that on delete of a user, the AssistanceRequest corresponding to them is
    # Also removed.
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    
    # We use 5 decimal places as this indicates 1 metre accuracy.
    latitude = models.DecimalField(decimal_places=5, max_digits=8)
    longitude = models.DecimalField(decimal_places=5, max_digits=8)
    lodge_time = models.DateTimeField(auto_now_add=True)
    request_details = models.TextField(max_length=200)

    is_finalized = models.BooleanField(default=False)
    
    def __str__(self):
        return self.creator.email + "\t" + self.request_details

    def isClosed(self):
        reqs = AssistanceApproval.objects.filter(request=self)
        for request in reqs:
            if request.is_approved:
                return True

        return False

    def isFinalized(self):
        return self.is_finalized

    def isApproved(self):
        reqs = AssistanceApproval.objects.filter(request=self)
        return reqs.count() > 0

    # Returns if the specified repairer responded to this request
    def isRespondedBy(self, prof):
        if self.isApproved():
            if (AssistanceApproval.objects.get(request=self).repairer.pk == prof.pk):
                return True

        return False
    
class AssistanceApproval(models.Model):
    repairer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    quote = models.DecimalField(decimal_places=2, max_digits=6)
    request = models.OneToOneField(AssistanceRequest, on_delete=models.CASCADE, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

# A review left for a user (either from a customer or an assistance professional)
class AssistanceReview(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='review_creator',
    )
    
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='review_target',
    )
    
    text_rating = models.TextField(max_length=200, blank=True, null=True)
    star_rating = models.IntegerField(default=5)

    def __str__(self):
        return creator.name + "->" + target.name + ": " + self.star_rating + ", " + self.text_rating

class PricingModel(models.Model):
    name = models.CharField(max_length=50)
    yearlyPrice = models.DecimalField(decimal_places=2, max_digits=5)
    calloutFee = models.DecimalField(decimal_places=2, max_digits=5)
    numCallouts = models.IntegerField()

    def __str__(self):
        return self.name

class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_at

# Represents a user profile model, which will be attached to all user models.
class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=50, blank=True)
    registration = models.CharField(max_length=20)
    isServicer = models.BooleanField(default=False)
    subscription = models.IntegerField(default=0)
    optionalDocument = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.get_full_name()