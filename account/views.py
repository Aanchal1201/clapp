from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from home.models import UserProfile
from quiz.models import LeaderBoard
from django.http import JsonResponse

# Create Registraton View 
def signup(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else:
        return render(request,'account/signup.html') 

def validate_registration(request):
    if request.method == 'POST':
        userExist = False
        emailExist = False
        success = False
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpass = request.POST['cpass']

        if User.objects.filter(username=username).exists():
            userExist = True
        if User.objects.filter(email=email).exists():
            emailExist = True
        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            myuser = User.objects.create_user(username,email,password)
            myuser.save()
            myprofile = UserProfile(UserUsername=myuser)
            myprofile.save()
            leaderBoard = LeaderBoard(user=myuser)
            leaderBoard.save()
            success = True
        json = {"success":success,"userExist":userExist,"emailExist":emailExist}
        return JsonResponse(json)
    else:
        return render(request,'home/404.html')
        

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else:
        return render(request,'account/login.html') 

def validate_login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        success = False
        userNotExist = False
        isPassIncorrect = False
        #check is user exists
        if email.find("@") == -1:
            username = email
            if not (User.objects.filter(username=username).exists()):
                userNotExist = True
        else:
            try:
                username = User.objects.get(email=email.lower()).username
            except User.DoesNotExist:
                userNotExist = True

        if User.objects.filter(username=username).exists():
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                success = True
            else:
                isPassIncorrect = True

        json = {"success":success,"userNotExist":userNotExist,"isPassIncorrect":isPassIncorrect}
        return JsonResponse(json)
    else:
        return render(request,'home/404.html')

def userLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('home')

def changePass(request):
    if request.user.is_authenticated:
        return render(request,'account/changePassword.html')
    else:
        return redirect('home')

def validate_change_password(request):
    if request.method == 'POST':
        oldPass = request.POST['oldPass']
        newPass = request.POST['newPass']
        cnewpass = request.POST['cnewpass']
        user = authenticate(username=request.user,password=oldPass) 
        success = False 
        if user is not None:
            user.set_password(newPass)
            user.save()
            login(request,user)
            success = True
        json = {"success":success}
        return JsonResponse(json)
    else:
        return render(request,'home/404.html')
            
            