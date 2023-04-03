from django.contrib import admin
from .models import Profile,Post

# Register your models here.
@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
    list_display = ['user','userid','bio','contact_no','country','city','dp']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user','image','caption','created_at','no_of_likes']