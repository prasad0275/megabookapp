from django.contrib import admin
from .models import Profile,Post,LikePost,FollowersCount

# Register your models here.
@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
    list_display = ['user','userid','bio','contact_no','country','city','dp']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user','image','caption','created_at','no_of_likes']

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['id','post_id','username']

@admin.register(FollowersCount)
class FollowersCountsAdmin(admin.ModelAdmin):
    list_display = ['id','follower','user']