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
    path('respond/<int:respond_pk>', views.respond_view, name='respond'),
	path('Terms_and_Conditions', views.TandC, name='TandC'),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


