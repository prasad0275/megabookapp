from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.urls import reverse
from .models import Profile,Post,LikePost,FollowersCount
import os
from django.conf import settings
# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    user_profile = Profile.objects.get(user = request.user)
    posts = Post.objects.order_by('-created_at')
    print(request.user.username)
    user_like_post = LikePost.objects.filter(username = request.user.username)
    following = FollowersCount.objects.filter(follower=request.user.username)
    user = []
    like_list = []
    following_list = []
    print(following)

    for i in following:
        u = User.objects.get(username=i)
        p = Profile.objects.get(user=u)
        following_list.append([u,p])

    print(following_list)
    # for i in following_list:
    #     print(i.username)
    
    for p in user_like_post:
        like_list.append(p.post_id)
    return render(request,'index.html',
                  {'user_profile' : user_profile,
                    'posts': posts,
                    'user_like_post':user_like_post,
                    'like_list':like_list,
                    'following_user_list':following_list,
                    'owner':1,
                    }) 

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
            messages.error(request,'Invalid Credentials')
            return redirect('/auth/login')
  
    return render(request,'login.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if(User.objects.filter(username = username).exists()):
            messages.error(request,'Username is already taken!')
            return redirect('/auth/signup')
        elif(User.objects.filter(email = email).exists()):
            messages.error(request,'Email is already exists!')
            return redirect('/auth/signup')
        elif(password != cpassword):
            messages.error(request,'Password not matched!')
            return redirect('/auth/signup')
        
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            messages.success(request,'User registered successfully, Please login')

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model,userid=user_model.id)
            new_profile.save()
            return redirect('/account/edit')

    return render(request,'signup.html')


@login_required(login_url='/auth/login')
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        user_model = auth.get_user_model()
        islogin = user_model.is_active
        print(islogin)
        return redirect('auth/login')
    
#The user watching its own profile
@login_required(login_url='/auth/login')
def account(request):
    user_profile = Profile.objects.get(user=request.user)
    user_model = User.objects.get(username = request.user)
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')
    image_id = request.GET.get("image")
    posts_count = Post.objects.filter(user=request.user).count()
    following_count = FollowersCount.objects.filter(follower=request.user).count()
    follower_count = FollowersCount.objects.filter(user=request.user).count()

    q_delete = request.GET.get("delete")
    if q_delete != None:
        print("delete")
        user_post_image = Post.objects.get(id=image_id)
        user_post_image.delete()
        return redirect('/account')

    print("image : ",image_id)
    if image_id != None:
        user_post_image = Post.objects.get(id=image_id)
        return render(request,'account.html',
                      {'user_profile':user_profile,
                       'user_model':user_model,
                       'user_posts':user_posts,
                       'user_post_image':user_post_image,
                       'owner':1,
                   'posts_count':posts_count,
                    'following_count':following_count,
                    'follower_count':follower_count,
                       })

    # print(user_posts.image)
    # if image != None:
    #     user_post_image = Post.objects.get(id=image)
    return render(request,'account.html',
                  {'user_profile':user_profile,
                   'user_model':user_model,
                   'user_posts':user_posts,
                   'owner':1,
                   'posts_count':posts_count,
                    'following_count':following_count,
                    'follower_count':follower_count
                    })

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

            # user_model.first_name = first_name
            # user_model.last_name = last_name
            # user_profile.bio = bio
            # user_profile.contact_no = contact_no
            # user_profile.country = country
            # user_profile.city = city

            # user_model.save()
            # user_profile.save()

        else:
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

@login_required(login_url='/auth/login')
def like_post(request):
    username = request.user.username
    post_id = request.POST.get('post_id')
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()

        if like_filter == None:
            new_post = LikePost.objects.create(post_id=post_id,username=username)
            new_post.save()
            post.no_of_likes += 1
            post.save()
            return redirect(reverse('index'))
        else:
            like_filter.delete()
            post.no_of_likes -= 1
            post.save()
            return redirect(reverse('index'))
        
#This is for user which are watching another user profile
def user_profile(request):
    owner = 0
    is_follow = 0
    user = request.GET.get('user')  
    user_model = User.objects.get(username=user)
    user_profile = Profile.objects.filter(user=user_model).first()
    user_posts = Post.objects.filter(user=user).order_by('-created_at')
    posts_count = Post.objects.filter(user=user).count()
    following_count = FollowersCount.objects.filter(follower=user).count()
    follower_count = FollowersCount.objects.filter(user=user).count()

    image_id = request.GET.get("image")
    if str(user_model.username) == str(request.user):
        owner = 1
        print(owner,'in if')

    if FollowersCount.objects.filter(follower=request.user,user=user).first():
        is_follow = 1

    print(owner,'in out')
    print('follow ' ,is_follow)
    if image_id != None:
        user_post_image = Post.objects.get(id=image_id)
        return render(request,'account.html',
                      {'user_profile':user_profile,
                       'user_model':user_model,
                       'user_posts':user_posts,
                       'user_post_image':user_post_image,
                       'is_follow':is_follow,

                       }
                      )

    return render(request,'account.html',
                  {'user_profile':user_profile,
                   'user_model':user_model,
                   'user_posts':user_posts,
                   'owner':owner,
                   'is_follow':is_follow,
                   'posts_count':posts_count,
                    'following_count':following_count,
                    'follower_count':follower_count,
                   })
    # return render(request,'account.html')

def follow(request):
    follower = str(request.user)
    user = request.GET.get('user')
    print('follower ',follower)
    print('user : ',user)

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        delete_follower = FollowersCount.objects.get(follower=follower,user=user)
        delete_follower.delete()
    else:
        FollowersCount.objects.create(follower=follower,user=user).save()
    
    return redirect(f'/profile?user={user}')

def search(request):

    search = request.GET.get('search')
    user_model = User.objects.filter(username__icontains=search)
    user_list = []
    user_profile = None
    if user_model is not None:
        for u in user_model:
            if u.is_superuser == False:
                user_profile = Profile.objects.filter(user=u).first()
                user_list.append(user_profile)
                # user_profile = user_profile.user
                print(user_profile.dp.url,user_profile.user.first_name)
    #     user_dp.append([u,user_profile.dp])
    # user_profile = Profile.objects.filter(user=user_model)
    # print(user_dp)

    # print(user_model.profile)
    return render(request,'search.html',
                  {
                   'user_profile':user_profile,
                   'user_list':user_list,
                   })

