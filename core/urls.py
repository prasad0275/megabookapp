from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('auth/login',views.login),
    path('auth/signup',views.signup),
    path('account',views.account),
    path('account/edit',views.account_edit),
    path('logout',views.logout),
    path('upload',views.upload),
]