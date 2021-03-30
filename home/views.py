from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from home.models import Contact,UserProfile
from django.contrib.auth.models import User

# Create your views here.

def handler404(request,exception):
    context = {}
    response = render(request, "home/404.html", context=context)
    response.status_code = 404
    return response
def privacyPolicy(request):
    return render(request,'home/privacyPolicy.html')
def termsconditions(request):
    return render(request,'home/termsConditions.html')
def faqs(request):
    return render(request,'home/faqs.html')
def userDashboard(request):
    return render(request,'home/userDashboard.html')


def home(request):
    # allposts = UserPost.objects.filter(adminStatus=True,userStatus="publish")[0:3]
    # context = {'allposts':allposts}
    # return render(request,'home/index.html',context)
    return render(request,'home/index.html')


def contact(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        if len(name)<2 or len(email)<2 or len(phone)<5 or len(desc)<2:
            messages.error(request,"Please fill your all details correctly")
        else:
            contact = Contact(name=name,email=email,phone=phone,desc=desc) 
            contact.save()
            messages.success(request,"Your message has been successfully sent")
            return redirect('home')            
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html') 

def viewProfile(request):
    myprofile = UserProfile.objects.get(UserUsername=request.user)
    myuser = User.objects.get(username=request.user)
    context = {"myuser":myuser,"myprofile":myprofile}
    return render(request,"home/viewProfile.html",context)

def editUserProfile(request):
    myprofile = UserProfile.objects.get(UserUsername=request.user)
    myuser = User.objects.get(username=request.user)
    context = {"myuser":myuser,"myprofile":myprofile}
    return render(request,'home/editUserProfile.html',context) 
    
def handleEditProfile(request):
    if request.method == 'POST':
        myprofile = UserProfile.objects.get(UserUsername=request.user)
        myuser = User.objects.get(username=request.user)
        myuser.first_name = request.POST['fname']
        myuser.last_name = request.POST['lname']
        myprofile.phoneNumber = request.POST['phone']
        myprofile.Gender = request.POST['gender']

        date = request.POST['dob']
        if date == "":
            myprofile.Dob = None
        else:
            myprofile.Dob = date
        
        myprofile.language = request.POST['language']
        myprofile.designation = request.POST['designation']
        myprofile.Country = request.POST['country']
        myprofile.State = request.POST['state']
        myprofile.District = request.POST['district']
        myprofile.city = request.POST['city']
        myprofile.address = request.POST['address']
        myprofile.pincode = request.POST['pincode']
        myprofile.Bio = request.POST['bio']
        pimage = request.FILES.get('pimage')

        if pimage is not None:
            myprofile.profileImage = pimage
        cimage = request.FILES.get('cimage')
        if cimage is not None:
            myprofile.coverImage = cimage
        
        myprofile.securityQues = request.POST['cques']
        myprofile.securityAns = request.POST['cans']
        myprofile.facebook_url = request.POST['facebook']
        myprofile.instagram_url = request.POST['instagram']
        myprofile.twitter_url = request.POST['twitter'] 
            
        myprofile.save()
        myuser.save()
        return redirect('viewProfile')

