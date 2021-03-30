from django.shortcuts import render,HttpResponse,redirect
from blog.models import UserPost
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from home.models import UserProfile

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def bloghome(request):
    allposts = UserPost.objects.filter(adminStatus=True,userStatus="publish").order_by('-dateUpdate')
    paginator = Paginator(allposts,9)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    
    context = {'page':page,'allposts':post_list}
    return render(request,'blog/blogHome.html',context)

def blogPost(request,slug):
    post = UserPost.objects.filter(slug=slug,userStatus="publish",adminStatus=True)
    if not request.user.is_authenticated:
        post = post.first()
    else:
        post1 = UserPost.objects.filter(slug=slug,authorUsername=request.user)
        post = post.union(post1).first()
    
    if post is not None:
        profile = UserProfile.objects.filter(UserUsername=post.authorUsername).first().profileImage
        prev_blog = UserPost.objects.filter(dateUpdate__gt=post.dateUpdate,userStatus="publish",adminStatus=True).order_by('dateUpdate').first()
        next_blog = UserPost.objects.filter(dateUpdate__lt=post.dateUpdate,userStatus="publish",adminStatus=True).order_by('-dateUpdate').first()
        
        context = {'post':post,"authorProfile":profile,"next":next_blog,"prev":prev_blog}
        return render(request,'blog/blogPost.html',context) 
    else:
        return HttpResponse("404 page not found")


def writeBlog(request):
    if request.user.is_authenticated:
        user_post = UserPost.objects.filter(authorUsername=request.user).order_by('-dateUpdate')
        return render(request,'blog/UserBlogs.html',{'allposts':user_post})
    else:
        return HttpResponse("404 page not found")  

def addBlog(request):
    if not request.user.is_authenticated:
        return HttpResponse("404 page not found")
    else: 
        return render(request,'blog/addBlog.html')
        
def handleAddBlog(request):
    if request.method == 'POST':
        title = request.POST['title']
        # Label = request.POST['Label']
        category = request.POST['category']
        content = request.POST['content']
        timeRead = request.POST['timeRead']
        image = request.FILES.get('image')
        status = request.POST['status']
        slug = str(title).replace(" ","-")

        if UserPost.objects.filter(slug=slug).exists():
            messages.error(request,"Your post title already exist, Please try with another one")
            return redirect('addBlog')
        else:
            USERPOST = UserPost(authorUsername=request.user,title=title,category=category,image=image,slug=slug,timeRead=timeRead,content=content,userStatus=status,adminStatus=False)
            USERPOST.save()
            messages.success(request,"User Blog is successfully created!!")
            return redirect('writeBlog')
    else:
        return HttpResponse("404 page not found")
        
def deleteUserBlog(request):
    if request.method == 'POST':
        delPost = UserPost.objects.get(slug=request.POST['del'])
        delPost.delete()
        return redirect('writeBlog')
    else:
        return HttpResponse("404 page not found")

def EditUserBlog(request):
    if request.method == 'POST':   
        editPost = UserPost.objects.get(slug=request.POST['edit'])
        context = {'post':editPost}
        return render(request,'blog/EditUserBlog.html',context)
    else:
        return HttpResponse("404 page not found")      

def handleEditUserBlog(request):
    if request.method == 'POST':
        editPost = UserPost.objects.get(slug=request.POST['slug'])
        editPost.title = request.POST['title']
        # editPost.label = request.POST['Label']
        editPost.category = request.POST['category']
        editPost.content = request.POST['content']
        editPost.timeRead = request.POST['timeRead']
        editPost.userStatus = request.POST['status']
        Image = request.FILES.get('image')
        if Image is not None:
            editPost.image = Image

        editPost.save()
        messages.success(request,"User Blog  is updated successfully!!")
        return redirect('writeBlog')
    else:
        return HttpResponse("404 page not found")
        
def search(request):
    query = request.GET['query']
    if len(query)>80:
        allposts = UserPost.objects.none()
    else:
        allpoststitle = UserPost.objects.filter(adminStatus=True,userStatus="publish",title__icontains=query)
        allpostscontent = UserPost.objects.filter(adminStatus=True,userStatus="publish",content__icontains=query)
        allposts = allpoststitle.union(allpostscontent).order_by('dateUpdate')
    
    if allposts.count()==0:
        messages.warning(request,"No search Results found!")
    context = {'allposts':allposts,'query':query}
    return render(request,'blog/searchBlog.html',context)

def viewAuthorProfile(request):
    myuser = User.objects.filter(username=request.user).first()
    if myuser is not None:
        myprofile = UserProfile.objects.get(UserUsername=request.user)
        user_post = UserPost.objects.filter(authorUsername=request.user)
        context = {"myuser":myuser,"myprofile":myprofile,"edit":True,'allposts':user_post}
        return render(request,'blog/ViewAuthorProfile.html',context)
    else:
        return HttpResponse("404 page not found")

def editAuthorProfile(request):
    myuser = User.objects.filter(username=request.user).first()
    if myuser is not None:
        myprofile = UserProfile.objects.filter(UserUsername=request.user).first()
        context = {"myuser":myuser,"myprofile":myprofile}
        return render(request,'blog/editAuthorProfile.html',context)
    else:
        return HttpResponse("404 page not found")

def handleEditAuthorProfile(request):
    if request.method == 'POST':
        myprofile = UserProfile.objects.get(UserUsername=request.user)
        myuser = User.objects.get(username=request.user)
        myuser.first_name = request.POST['fname']
        myuser.last_name = request.POST['lname']
      
        myprofile.Gender = request.POST['gender']

        date = request.POST['dob']
        if date == "":
            myprofile.Dob = None
        else:
            myprofile.Dob = date
        
        myprofile.language = request.POST['language']
        myprofile.designation = request.POST['designation']
        myprofile.Country = request.POST['country']
       
        myprofile.city = request.POST['city']
        
        myprofile.Bio = request.POST['bio']
        pimage = request.FILES.get('pimage')

        if pimage is not None:
            myprofile.profileImage = pimage
        cimage = request.FILES.get('cimage')
        if cimage is not None:
            myprofile.coverImage = cimage
        
        myprofile.facebook_url = request.POST['facebook']
        myprofile.instagram_url = request.POST['instagram']
        myprofile.twitter_url = request.POST['twitter']

        public = request.POST.get('public',False)
        if public == "on":
            myprofile.isPublic = True
        else:
            myprofile.isPublic = False
            
        myprofile.save()
        myuser.save()
        return redirect('viewAuthorProfile')
    else:
        return HttpResponse("404 page not found")

def viewProfile(request,profile):
    myuser = User.objects.filter(username=profile).first()
    if myuser is not None:
        myprofile =  UserProfile.objects.filter(UserUsername=myuser,isPublic=True).first()
        if myprofile is None:
            myprofile = UserProfile.objects.filter(UserUsername=myuser).first()
            context = {"profileHide":True,"username":myuser.username}
            return render(request,'blog/ViewAuthorProfile.html',context)
        else:
            user_post = UserPost.objects.filter(authorUsername=myuser,adminStatus=True,userStatus="publish")
            context = {"myuser":myuser,"myprofile":myprofile,'allposts':user_post}
            return render(request,'blog/ViewAuthorProfile.html',context)
    else:
        return HttpResponse("404 page not found")
