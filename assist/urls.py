from django.urls import include, path
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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
