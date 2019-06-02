from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lodge', views.lodge, name='lodge'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('profile', views.profile_view, name='profile'),
    path('signup', views.signup_view, name='signup'),
    path('dash', views.dash_view, name='dash'),
    re_path(r'^withdraw/(?P<withdraw_pk>[0-9]+)/$', views.withdraw_view, name='withdraw'),
    path('reports', views.reports_view, name='reports'),
    path('reports/payment', views.payment_report_view, name='payment_report'),
    path('report/service', views.service_report_view, name='service_report'),
    path('ratings/view/<int:profile_id>', views.ratings_view, name='ratings'),
    path('response/view/<int:request_pk>', views.view_responses, name='view_responses'),
    path('response/remove/<int:approval_pk>', views.remove_response, name='remove_response'),
    path('response/accept/<int:approval_pk>', views.approve_response, name='approve_response'),
    path('response/finalize/<int:request_pk>', views.finalize_request, name='finalize_request'),
    path('respond/withdraw/<int:request_pk>', views.withdraw_response_view, name='withdraw_response'),
    path('respond/<int:respond_pk>', views.respond_view, name='respond'),
	path('Terms_and_Conditions', views.TandC, name='TandC'),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


