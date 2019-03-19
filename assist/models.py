from django.conf import settings
from django.db import models

# All the models that are required for the maintenance booking engine are defined here.
# For those not familiar with Django, all data sets are assosciated with models

# A request made for assistance
class AssistanceRequest(models.Model):
    
    # We cascade so that on delete of a user, the AssistanceRequest corresponding to them is
    # Also removed.
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    # We use 5 decimal places as this indicates 1 metre accuracy.
    latitude = models.DecimalField(decimal_places=5, max_digits=8)
    longitude = models.DecimalField(decimal_places=5, max_digits=8)
    lodge_time = models.DateTimeField()
    request_details = models.TextField(max_length=200)
    
    def __str__(self):
        return self.creator.email + "\t" + self.request_details
    
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
        related_name='review_target',
    )
    
    star_rating = models.IntegerField(default=5)

class PricingModel(models.Model):
    name = models.CharField(max_length=50)
    yearlyPrice = models.DecimalField(decimal_places=2, max_digits=5)
    calloutFee = models.DecimalField(decimal_places=2, max_digits=5)
    numCallouts = models.IntegerField()

    def __str__(self):
        return self.name