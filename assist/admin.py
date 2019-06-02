from django.contrib import admin

from .models import *

admin.site.site_header = "EzyAssist Administration"
admin.site.site_title = "EzyAssist Admin"

# Register your models here.
@admin.register(AssistanceRequest)
class AssistanceRequest(admin.ModelAdmin):
    list_display = ('creator_name', 'latitude', 'longitude', 'request_details')
    date_hierarchy = 'lodge_time'

    def creator_name(self, obj):
        return ("%s %s" % (obj.creator.first_name, obj.creator.last_name))
    creator_name.short_description = 'Lodger'

@admin.register(UserProfileModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'isServicer', 'address', 'document_url')
    search_fields = ('user__first_name',)
    actions = ("revoke_servicer",)

    def revoke_servicer(self, request, queryset):
        queryset.update(isServicer=False)
    revoke_servicer.short_description="Revoke Servicer Status"

    def document_url(self, obj):
        if (obj.optionalDocument):
            return (obj.optionalDocument.document)
        else:
            return "Not a Servicer"
    document_url.short_description = "Document URL"

    def user_name(self, obj):
        return ("%s %s" % (obj.user.first_name, obj.user.last_name))
    user_name.short_description = 'User Name'

@admin.register(AssistanceApproval)
class ApprovalAdmin(admin.ModelAdmin):
    search_fields = ('repairer__first_name',)
    list_display = ('repairer_name', 'quote', 'is_approved',)
    actions=('make_not_approved',)

    def make_not_approved(self, request, queryset):
        queryset.update(is_approved=False)
    make_not_approved.short_description = "Unnapprove selected items"

    def repairer_name(self, obj):
        return ("%s %s" % (obj.repairer.first_name, obj.repairer.last_name))
    repairer_name.short_description = 'Repairer Name'


@admin.register(AssistanceReview)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('target__first_name',)
    list_display = ('origin_name', 'target_name', 'star_rating',)

    def origin_name(self, obj):
        return ("%s %s" % (obj.creator.first_name, obj.creator.last_name))
    origin_name.short_description = 'From'

    def target_name(self, obj):
        return ("%s %s" % (obj.target.first_name, obj.target.last_name))
    target_name.short_description = 'To'

admin.site.register(PricingModel)
admin.site.register(Document)