from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from blog.models import UserPost
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from home.models import UserProfile
from contrib.models import *
from quiz.models import Language

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def contribHome(request):
    if request.user.is_authenticated:
        blogs = UserPost.objects.filter(authorUsername=request.user).order_by('-dateUpdate').count()
        uLang = userLanguage.objects.filter(userName=request.user)
        sLang = userSnippetLanguage.objects.filter(userName=request.user)
        qCount = 0
        sCount = 0
        for lang in uLang:
            quizCount = userQues.objects.filter(userLang=lang).count()
            qCount += quizCount
        for lang in sLang:
            snipCount = userSnip.objects.filter(userLang=lang).count()
            sCount += snipCount
        context = {"blogCount":blogs,"quizCount":qCount,"snippetCount":sCount}
        return render(request,'contrib/home.html',context)
    else:
        return redirect('/account/login')

def contribBlog(request):
    if request.user.is_authenticated:
        user_post = UserPost.objects.filter(authorUsername=request.user).order_by('-dateUpdate')
        return render(request,'contrib/BlogHome.html',{'allposts':user_post})
    else:
        return redirect('/account/login')
def contribQuiz(request):
    if request.user.is_authenticated:
        userLang = userLanguage.objects.filter(userName=request.user)

        allLangs = set(Language.objects.values_list('language', flat=True))
        userLangs = set(userLanguage.objects.values_list('language', flat=True))
        notuserLangs = list(allLangs - userLangs)

        context = {"userLang":userLang,"notuserLang":notuserLangs}
        return render(request,'contrib/QuizHome.html',context)
    else:
        return redirect('/account/login')

def contribsnippet(request):
    if request.user.is_authenticated:
        userLang = userSnippetLanguage.objects.filter(userName=request.user)

        allLangs = set(Language.objects.values_list('language', flat=True))
        userLangs = set(userSnippetLanguage.objects.values_list('language', flat=True))
        notuserLangs = list(allLangs - userLangs)

        context = {"userLang":userLang,"notuserLang":notuserLangs}
        return render(request,'contrib/SnippetHome.html',context)
    else:
        return redirect('/account/login')

def addLang(request):
    if request.method == 'POST' and request.user.is_authenticated:
        lang = request.POST['lang']
        langObj = userLanguage(language=lang,userName=request.user)
        langObj.save()
        return redirect('contribQuiz')

def quizQues(request,lang):
    if request.user.is_authenticated:
        LanguageExist = userLanguage.objects.filter(language=lang,userName=request.user).first()
        if LanguageExist is not None:
            allQues = userQues.objects.filter(userLang=LanguageExist)
            context = {"lang":lang,"allQues":allQues}
            return render(request,'contrib/QuizQues.html',context)
        else:
            return HttpResponse("404 page not found")

def addQues(request,lang):
    if request.method == 'POST':
        Ques = request.POST['ques']
        choice1 = request.POST['choice1']
        choice2 = request.POST['choice2']
        choice3 = request.POST['choice3']
        choice4 = request.POST['choice4']
        Ans = request.POST['ans']
        LanguageExist = userLanguage.objects.filter(language=lang,userName=request.user).first()
        LanguageExist.quesCount += 1
        LanguageExist.save()
        if LanguageExist is not None:
            myQues = userQues(Ques=Ques,choice1=choice1,choice2=choice2,choice3=choice3,choice4=choice4,Ans=Ans,userLang=LanguageExist)
            myQues.save()
            return HttpResponseRedirect(f'/contribution/quiz/{lang}')

def deleteQues(request,lang,id):
    if request.method == 'POST':
        LanguageExist = userLanguage.objects.filter(language=lang,userName=request.user).first()
        LanguageExist.quesCount -= 1
        LanguageExist.save()
        deleteQues = userQues.objects.filter(userLang=LanguageExist,id=id)
        deleteQues.delete()
        return HttpResponseRedirect(f'/contribution/quiz/{lang}')

def EditQues(request,lang,id):
    if request.method == 'POST':
        LanguageExist = userLanguage.objects.filter(language=lang,userName=request.user).first()
        editQues = userQues.objects.filter(userLang=LanguageExist,id=id).first()
        editQues.Ques = request.POST['ques']
        editQues.choice1 = request.POST['choice1']
        editQues.choice2 = request.POST['choice2']
        editQues.choice3 = request.POST['choice3']
        editQues.choice4 = request.POST['choice4']
        editQues.Ans = request.POST['ans']
        editQues.save()
        return HttpResponseRedirect(f'/contribution/quiz/{lang}')

def snippetLang(request,lang):
    if request.user.is_authenticated:
        LanguageExist = userSnippetLanguage.objects.filter(language=lang,userName=request.user).first()
        if LanguageExist is not None:
            allsnips = userSnip.objects.filter(userLang=LanguageExist)
            context = {"lang":lang,"allsnips":allsnips}
            return render(request,'contrib/snippetLang.html',context)
        else:
            return HttpResponse("404 page not found")

def addSnippetLang(request):
    if request.method == 'POST' and request.user.is_authenticated:
        lang = request.POST['lang']
        langObj = userSnippetLanguage(language=lang,userName=request.user)
        langObj.save()
        return redirect('contribsnippet')
        
def addSnip(request,lang):
    if request.method == 'POST':
        title = request.POST['title']
        snip = request.POST['snip']
        summary = request.POST['summary']
        LanguageExist = userSnippetLanguage.objects.filter(language=lang,userName=request.user).first()
        LanguageExist.snippetCount += 1
        LanguageExist.save()
        if LanguageExist is not None:
            mysnip = userSnip(userLang=LanguageExist,title=title,code=snip,summary=summary)
            mysnip.save()
            return HttpResponseRedirect(f'/contribution/snippet/{lang}')
        
def deleteSnip(request,lang,id):
    if request.method == 'POST':
        LanguageExist = userSnippetLanguage.objects.filter(language=lang,userName=request.user).first()
        LanguageExist.snippetCount -= 1
        LanguageExist.save()
        deleteQues = userSnip.objects.filter(userLang=LanguageExist,id=id)
        deleteQues.delete()
        return HttpResponseRedirect(f'/contribution/snippet/{lang}')


def editSnip(request,lang,id):
    if request.method == 'POST':
        LanguageExist = userSnippetLanguage.objects.filter(language=lang,userName=request.user).first()
        editQues = userSnip.objects.filter(userLang=LanguageExist,id=id).first()
        editQues.title = request.POST['title']
        editQues.code = request.POST['snip']
        editQues.summary = request.POST['summary']
        editQues.save()
        return HttpResponseRedirect(f'/contribution/snippet/{lang}')
