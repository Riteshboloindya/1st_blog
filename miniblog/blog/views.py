from django.shortcuts import render 
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .forms import SignUpForm, LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post, get_upload_path
from django.core.files.storage import DefaultStorage


# home

def home(request):
    posts=Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})
#about
def about(request):
    return render(request,'blog/about.html')

#contact
def contact(request):
    return render(request,'blog/contact.html')


#Dashbord

def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        return render(request,'blog/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/')

#logout
def user_logout(request):
    logout(request)
    return  redirect('/')



#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form =LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname =form.cleaned_data['username']
                upass =form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

#signup
def user_signup(request):
    if request.method== "POST":
        form =SignUpForm(request.POST )
        if form.is_valid():
            messages.success(request,'congratulation!! you are  memeber')
            form.save()
    else:
        form = SignUpForm()
           
    return render(request,'blog/signup.html',{'form':form})

# Add new post

def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form =PostForm(request.POST)
            print('request.FILES',request.FILES)
            img = request.FILES.get('post_img',None)    
            print('file',img)
            if form.is_valid():
                print('form data',form)
                # title=form.cleaned_data['title']
                # desc =form.cleaned_data['desc']
                
                # pst =Post(title=title,desc=desc)
                # pst.save()
                post = form.save()
                print('post',post,post.title)
                if img is not None:
                    print('uploading img')
                    fs = DefaultStorage()
                    path = get_upload_path(post,img.name)
                    file = fs.save(path,img)
                    post.post_img = file
                    post.save()

                # form = PostForm()
            else:
                form =PostForm
                return render(request,'blog/addpost.html',{'form':form})
        else:
            form =PostForm
            return render(request,'blog/addpost.html',{'form':form})
        #  else:
    return HttpResponseRedirect('/login/')

# Update post

def update_post(request,id):
    if request.user.is_authenticated:
        return render(request,'blog/updatepost.html')
    else:
        return HttpResponseRedirect('/login/')

# Delete post
def delete_post(request,id):
    if request.user.is_authenticated:
        print('post id',id)
        try:
            p = Post.objects.get(pk=id)
            p.delete()
        except Post.DoesNotExist:
            print('object does not exist')
            return HttpResponseRedirect('/dashboard/')    
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')