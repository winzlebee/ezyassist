from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lodge', views.lodge, name='lodge'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup')
]
