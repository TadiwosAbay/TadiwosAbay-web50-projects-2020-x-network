import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import AllPosts,followed,likes
from .models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required





@login_required
def index(request):
    if request.method=='POST':
            post=request.POST["content"]
            user = AllPosts.objects.create(user=request.user,post=post)
            user.save()
    posts=AllPosts.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page = request.GET.get('page',1)
    page_objs = paginator.page(page)
    return render(request, "network/index.html",{
           "page_objs":page_objs
        })

@login_required
def profile(request,useee):
    user=int(useee)
    posts=AllPosts.objects.filter(user=user).order_by("-timestamp")
    post=posts[0]
    paginator = Paginator(posts, 10)
    page = request.GET.get('page',1)
    page_objs = paginator.page(page)
    followers=followed.objects.filter(followeds=post.user).count()
    followeds=followed.objects.filter(user=post.user).count()
    if(request.user == post.user):
         return render(request,"network/profiles.html",{
           "page_objs":page_objs,"followers":followers,"followeds":followeds,"post":post
        })
    else:
        return render(request,"network/profile.html",{
           "page_objs":page_objs,"followers":followers,"followeds":followeds,"post":post
        })

@login_required
def edited(request,id,edited):
    id=int(id)
    poster=AllPosts.objects.get(pk=id).user
    if request.user==poster:
         AllPosts.objects.filter(pk=id).update(post=edited)
         posts=AllPosts.objects.filter(pk=id)
         post=posts[0].post
         return JsonResponse({'post': post})
    else:
        return JsonResponse({'post':"You can't edit another user's post"})

@login_required
def follow(request,user):
    useee=int(user)
    posts=AllPosts.objects.filter(user=useee)
    post=posts[0]

    if request.method=="POST":
        there=followed.objects.filter(user=request.user,followeds=post.user)
        if there:
            there.delete()
        else:
            user = followed.objects.create(user=request.user,followeds=post.user)
            user.save()
    follower=followed.objects.filter(followeds=post.user).count()
    followeds=followed.objects.filter(user=post.user).count()
    return HttpResponseRedirect(reverse('profile',args=(useee,)))

@login_required
def following(request):
    posts=AllPosts.objects.all().order_by("-timestamp")
    follows=followed.objects.filter(user=request.user)
    books=[]
    names=[]
    for follow in follows:
        books.append(follow.followeds)
    for post in posts:
        if post.user in books:
           names.append(post)
    paginator = Paginator(names, 10)
    page = request.GET.get('page',1)
    page_objs = paginator.page(page)
    return render(request,"network/following.html",{
       "page_objs":page_objs
    })

@login_required
def pros(request,id):
    posts=AllPosts.objects.filter(pk=id)
    post=posts[0]
    like=post.like
    present=likes.objects.filter(post=post,liked_by=request.user)
    if present:
           present.delete()
           x=like-1

           AllPosts.objects.filter(pk=id).update(like=x)
           posts=AllPosts.objects.filter(pk=id)
           post=posts[0]
           like=post.like


    else:
        Likes=likes(
            post=post,
            liked_by=request.user
          )
        Likes.save()
        x=like+1

        AllPosts.objects.filter(pk=id).update(like=x)
        posts=AllPosts.objects.filter(pk=id)
        post=posts[0]
        like=post.like
    return JsonResponse({'like': like})







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
    return HttpResponseRedirect(reverse("login"))


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
