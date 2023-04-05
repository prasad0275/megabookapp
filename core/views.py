from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from .models import Profile,Post
import os
from django.conf import settings
# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    user_profile = Profile.objects.get(user = request.user)
    posts = Post.objects.order_by('-created_at')
    return render(request,'index.html',{'user_profile' : user_profile,'posts': posts}) 

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            user_model = User.objects.get(username=username)
            profile_model = Profile.objects.get(userid=user_model.id)
            print("model :",profile_model.user)
            user_dic = { 'profile_info' : profile_model,'login':True}
            return redirect('/',user_dic)
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/auth/login')

    
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if(password != cpassword):
            messages.info(request,'Password not matched!')
            return redirect('/auth/signup')

        elif(User.objects.filter(email = email).exists()):
            messages.info(request,'Email is already exists!')
            return redirect('/auth/signup')
        
        elif(User.objects.filter(username = username).exists()):
            messages.info(request,'Username is already taken!')
            return redirect('/auth/signup')
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model,userid=user_model.id)
            new_profile.save()
            return redirect('/account/edit')

    return render(request,'signup.html')

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        user_model = auth.get_user_model()
        islogin = user_model.is_active
        print(islogin)
        return redirect('auth/login')
    
@login_required(login_url='/auth/login')
def account(request):
    user_profile = Profile.objects.get(user=request.user)
    user_model = User.objects.get(username = request.user)
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')
    image_id = request.GET.get("image")

    q_delete = request.GET.get("delete")
    if q_delete != None:
        print("delete")
        user_post_image = Post.objects.get(id=image_id)
        user_post_image.delete()
        return redirect('/account')

    print("image : ",image_id)
    if image_id != None:
        user_post_image = Post.objects.get(id=image_id)
        return render(request,'account.html',{'user_profile':user_profile,'user_model':user_model,'user_posts':user_posts,'user_post_image':user_post_image})

    # print(user_posts.image)
    # if image != None:
    #     user_post_image = Post.objects.get(id=image)
    return render(request,'account.html',{'user_profile':user_profile,'user_model':user_model,'user_posts':user_posts})

@login_required(login_url='/auth/login')
def account_edit(request):
    print(request.user)
    user_profile = Profile.objects.get(user=request.user)
    user_model = User.objects.get(username=request.user)
    print(user_model.email)
    if request.method == 'POST':
        # dp = request.POST['dp']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        bio = request.POST['bio']
        contact_no = request.POST['contact_no']
        country = request.POST['country']
        city = request.POST['city']

        if contact_no == '':
            contact_no  = None
        if request.FILES.get('dp') == None:
            dp = user_profile.dp
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_profile.bio = bio
            user_profile.contact_no = contact_no
            user_profile.country = country
            user_profile.city = city

            user_model.save()
            user_profile.save()

        if request.FILES.get('dp') != None:
            dp = request.FILES.get('dp')
            user_profile.dp = dp
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_profile.bio = bio
            user_profile.contact_no = contact_no
            user_profile.country = country
            user_profile.city = city

            user_model.save()
            user_profile.save()
            
        
    
        pass
    return render(request,'account_edit.html',{'user_profile':user_profile,'user_model':user_model})

@login_required(login_url='/auth/login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        print("user ",user)
        image = request.FILES.get('image_upload')
        print("image ",image)
        caption = request.POST['caption']
        print("caption ",caption)

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        print("new_post ",new_post)
        new_post.save()
        if new_post != None:
            messages.info(request,'Image successfully posted!')
        else:
            messages.info(request,'Error, Please try again!')
    else:
        pass
        # redirect('/')

    return redirect('/')