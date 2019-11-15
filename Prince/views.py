from django.shortcuts import render,redirect,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post,Comment
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from .forms import Signupform,loginForm,ProfileForm,UserRegistrationForm,CommentForm
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

def post_list(request):
    posts=Post.object.all()
    query=request.GET.get('search')
    if query:
        posts=Post.object.filter(Q(author__username=query)|
                                 Q(title__contains=query)|
                                 Q(body__contains=query))

    return render(request,'photo_list.html',{'posts':posts})






def signup(request):
    if request.method=='POST':
        form = Signupform(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('posts')

    else:
        form=Signupform()

    return render(request,'signup.html',{'form':form})

def login_user(request):
    if request.method=="POST":
        form=loginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    messages.success(request,"Logged in as {}".format(username))
                    return HttpResponseRedirect(reverse('posts'))
                else:
                    return HttpResponse("User is not Active")
            else:
                return HttpResponseRedirect(reverse('login'))

    else:
        form=loginForm()

    return render(request,'login.html',{'form':form})



def logout_request(request):
    logout(request)
    messages.info(request,'logged out successfully..!!!!')
    return redirect('posts')



def detail_post(request,id,slug):
    posts=get_object_or_404(Post,id=id,slug=slug)
    calc=posts.likes.count()
    calc2=calc-1
    comments=Comment.objects.filter(post=posts,reply=None).order_by('-id')
    is_liked=False
    if posts.likes.filter(id=request.user.id).exists():
        is_liked=True
    is_favourite = False
    if posts.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method=="POST":
        commentform=CommentForm(request.POST or None)
        if commentform.is_valid():

            content=request.POST.get('content')
            reply_id=request.POST.get('reply_id')
            comment_qs=None
            if reply_id:
                comment_qs=Comment.objects.get(id=reply_id)
            comment=Comment.objects.create(post=posts,user=request.user,content=content,reply=comment_qs)
            comment.save()
            #return redirect(posts.get_absolute_url())
    else:
         commentform=CommentForm()

    context={'posts':posts,
             'is_liked':is_liked,
             'calc2':calc2,
             'is_favourite':is_favourite,
             'comments':comments,
             'commentform':commentform}

    if request.is_ajax():
        html=render_to_string('includes/comment_forms.html',context,request)
        return JsonResponse({'form':html})
    return render(request,'post_detail.html',context)

def like_post(request):
    posts=get_object_or_404(Post,id=request.POST.get('post_id'))


    is_liked=False
    if posts.likes.filter(id=request.user.id).exists():
        posts.likes.remove(request.user)
        is_liked=False
    else:
        posts.likes.add(request.user)
        is_liked=True
    return HttpResponseRedirect(posts.get_absolute_url())


@login_required()
def editProfile(request):

    if request.method=='POST':
        form=UserRegistrationForm(data=request.POST or None,instance=request.user)
        form2=ProfileForm(data=request.POST or None,instance=request.user.profile,files=request.FILES)

        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('posts')

    else:
        form=UserRegistrationForm(instance=request.user)
        form2=ProfileForm(instance=request.user)

    return render(request,'edit_profile.html',{'form':form,'form2':form2})

def favouriteView(request,id):
    posts=get_object_or_404(Post,id=id)
    if posts.favourite.filter(id=request.user.id).exists():
        posts.favourite.remove(request.user)
    else:
        posts.favourite.add(request.user)

    return redirect(posts.get_absolute_url())
