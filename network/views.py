from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User,Post,Follow,Like
from django.shortcuts import get_object_or_404
import json

def remove_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"success": True, "message": "Like removed successfully"})

def add_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    new_like = Like(user=user, post=post)
    new_like.save()
    return JsonResponse({"success": True, "message": "Like added successfully"})
    

def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    followingPeople = Follow.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by('id').reverse()
    followingPosts = []
    for post in allPosts:
        for person in followingPeople:
            if person.user_follower == post.user:
                followingPosts.append(post)

    paginator = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts_of_the_page": posts_of_the_page
    })


def edit(request,post_id):
    if request.method=="POST":
        data=json.loads(request.body)
        edit_post=Post.objects.get(pk=post_id)
        edit_post.content=data['content']
        edit_post.save()
        return JsonResponse({"message":"Change successful","data":data["content"]})

def index(request):
    following_posts=Post.objects.all().order_by("id").reverse()

    paginator=Paginator(following_posts,10)
    page_number=request.GET.get('page')
    posts_of_the_page=paginator.get_page(page_number)
    allLikes=Like.objects.all()
    whoYouLiked=[]
    try:
        for like in allLikes:
            if like.user.id==request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked=[]

    return render(request, "network/index.html",{
        'following_posts':following_posts,
        "posts_of_the_page":posts_of_the_page,
        "whoYouLiked":whoYouLiked,
    })

def follow(request):
    userfollow=request.POST['userfollow']
    currentUser=User.objects.get(pk=request.user.id)
    userfollowData=User.objects.get(username=userfollow)
    f=Follow(user=currentUser,user_follower=userfollowData)
    f.save()
    user_id=userfollowData.id
    return HttpResponseRedirect(reverse(profile,kwargs={'user_id':user_id}))

def unfollow(request):
    userfollow=request.POST['userfollow']
    currentUser=User.objects.get(pk=request.user.id)
    userfollowData=User.objects.get(username=userfollow)
    f=Follow.objects.get(user=currentUser,user_follower=userfollowData)
    f.delete()
    user_id=userfollowData.id
    return HttpResponseRedirect(reverse(profile,kwargs={'user_id':user_id}))


def newPost(request):
    if request.method=="POST":
        content=request.POST['content']
        user=User.objects.get(pk=request.user.id)
        post=Post(content=content,user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))

def profile(request,user_id):
    user=User.objects.get(pk=user_id)
    following_posts=Post.objects.filter(user=user).order_by("id").reverse()

    following=Follow.objects.filter(user=user)
    followers=Follow.objects.filter(user_follower=user)

    paginator=Paginator(following_posts,10)
    page_number=request.GET.get('page')
    posts_of_the_page=paginator.get_page(page_number)

    try:
        checkFollow=followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) !=0:
            isFollowing=True
        else:
            isFollowing=False
    except:
        isFollowing=False
        
    return render(request, "network/profile.html",{
        'following_posts':following_posts,
        "posts_of_the_page":posts_of_the_page,
        'username':user.username,
        "following":following,
        "followers":followers,
        "isFollowing":isFollowing,
        "user_profile":user,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
