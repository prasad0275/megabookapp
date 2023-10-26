from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('auth/login',views.login),
    path('auth/signup',views.signup),
    path('account',views.account),
    path('account/edit',views.account_edit),
    path('logout',views.logout),
    path('upload',views.upload),
    path('like-post',views.like_post),
    path('profile/',views.user_profile),
    path('follow',views.follow),
    path('search',views.search),

]