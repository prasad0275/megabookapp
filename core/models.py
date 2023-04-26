from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid
# Create your models here.
User = get_user_model()
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    userid = models.IntegerField(blank=True,null=True)
    bio = models.TextField(blank=True,null=True,default='')
    contact_no = models.IntegerField(blank=True,null=True)
    country  = models.CharField(max_length=32,blank=True,null=True,default='')
    city = models.CharField(max_length=32,blank=True,null=True,default='')
    dp = models.ImageField(upload_to='dps',default='user.png',blank=True,null=True)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images',default='first.PNG')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user