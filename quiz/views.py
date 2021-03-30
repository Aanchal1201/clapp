from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from quiz.models import *
# Create your views here.

def startQuiz(request):
    languages = Language.objects.all()
    allTitles = []
    for lang in languages:
        user_play = []
        noOfQues = []
        titles = Title.objects.filter(Language=lang).order_by('-created')[:4]
        for title in titles:
            ques = Quiz.objects.filter(title=title).count()
            noOfQues.append(ques)
            if request.user.is_authenticated:
                userScore = UserScore.objects.filter(quizUsername=request.user,quizTitle=title).first()
                if userScore is not None:
                    userplay = "True"
                else:
                    userplay = "False"
                user_play.append(userplay)
            else:
                user_play = "False"

        allTitles.append(zip(titles,user_play,noOfQues))
    context = {"allTitles":allTitles}
    return render(request,'quiz/quizHome.html',context)

def quizInstruction(request,slug):
    if request.method == 'POST':
        Title1 = Title.objects.filter(title=slug).first()
        myquiz = Quiz.objects.filter(title=Title1).count()
        if myquiz > 0:
            context = {"count":myquiz,"time":Title1.timeTaken,"title":Title1.title}
            
        else:
            context = {"blank":True} 
        return render(request,'quiz/quizInstructions.html',context)
    else:
        return HttpResponse("404 Page not found")  

def quizStart(request,slug):
    if request.method == "POST":
        Title1 = Title.objects.filter(title=slug).first()
        myquiz = Quiz.objects.filter(title=Title1)
        if myquiz is not None:
            context = {"myquiz":myquiz,"count":myquiz.count()}
            return render(request,'quiz/quizStart.html',context)            
    return HttpResponse("404 Page not Found")

def handleQuiz(request):
    if request.method == 'POST':
        n = int(request.POST['count'])
        score = 0
        json = ''
        total_incorrect = 0
        total_unanswered = 0
        time_remaining = request.POST['time']
        for i in range(1,n+1):
            q = request.POST[str(i)]
            qz = request.POST.get('quiz'+str(i))
            userquiz = Quiz.objects.filter(Ques=q).first()

            if (userquiz.Ans == qz):
                score += 1
                is_correct = "true"
            elif (qz == None):
                total_unanswered += 1
                is_correct = "unanswered"
            else:
                is_correct = "false"

            json += '{' + f'"Ques":"{userquiz.Ques}","choice1":"{userquiz.choice1}","choice2":"{userquiz.choice2}","choice3":"{userquiz.choice3}","choice4":"{userquiz.choice4}","Ans":"{userquiz.Ans}","userAns":"{qz}","is_correct":"{is_correct}"' + '},'
            title = userquiz.title
            
        json_data = "[" + json[0:-1] + "]"
        total_incorrect = n - score - total_unanswered
        userID = 0
        timeTaken = title.timeTaken
        if time_remaining == "-1:-1" or time_remaining == "00:00" or time_remaining == f'{timeTaken}:00':
            time_consume = f'{timeTaken}:00'
        else:
            time = time_remaining.split(":")
            mins =  int(timeTaken)-1-int(time[0])
            secs = 60-int(time[1])
            min = mins if len(str(mins)) > 1 else ("0" + str(mins))
            sec = secs if len(str(secs)) > 1 else ("0" + str(secs)) 
            time_consume = f'{min}:{sec}'
        if request.user.is_authenticated:
            userLeaderboard = LeaderBoard.objects.filter(user=request.user).first()
            userLeaderboard.current_score += score
            userLeaderboard.save()
            userScore = UserScore(quizUsername=request.user,quizTitle=title,user_score=score,total_score=n,total_correct=score,total_incorrect=total_incorrect,total_unanswered=total_unanswered,time_consume=time_consume,quiz_data=json_data)
            userScore.save()  
            if userScore.id == None:
                userID = 0
            else:
                userID = userScore.id
            return HttpResponseRedirect(f'/quiz/quizScore/{userID}')
            
        context = {"title":title,"user_score":score,"total_score":n,"unanswered":total_unanswered,"time":time_consume,"id":userID,"notGiveFeedback":True}
        return render(request,'quiz/quizResult.html',context)
    else:
        return HttpResponse("404 page not found")

def viewAnswer(request,id):
    if id == 0:
        isNotUser = True
        context = {"isNotUser":isNotUser}
    else:
        userscore = UserScore.objects.filter(id=id,quizUsername=request.user).first()
        if userscore is not None:
            isNotUser = False
            context = {"isNotUser":isNotUser,"userscore":userscore}
        else:
            isNotUser = True
            context = {"isNotUser":isNotUser}
    return render(request,'quiz/quizScore.html',context)

def quizScore(request,id):
    if id == 0:
        isNotUser = True
        context = {"isNotUser":isNotUser}
    else:
        userscore = UserScore.objects.filter(id=id,quizUsername=request.user).first()
        if userscore is not None:
            isNotUser = False
            context = {"title":userscore.quizTitle,"user_score":userscore.user_score,"total_score":userscore.total_score,"unanswered":userscore.total_unanswered,"time":userscore.time_consume,"id":userscore.id,"notGiveFeedback":True}
        else:
            isNotUser = True
            context = {"isNotUser":isNotUser}
    return render(request,'quiz/quizResult.html',context)

def viewScore(request):
    if request.user.is_authenticated:
        userScore = UserScore.objects.filter(quizUsername=request.user).order_by('-played_date')
        if userScore.count() != 0:
            context = {"userscore":userScore}
        else:
            context = {"notPlay":True}
        return render(request,'quiz/UserScore.html',context)

def category(request,slug):
    user_play = []
    noOfQues = []
    title = Title.objects.filter(Language=slug).order_by('-created')
    for tit in title:
        ques = Quiz.objects.filter(title=tit).count()
        noOfQues.append(ques)
        if request.user.is_authenticated:
            userScore = UserScore.objects.filter(quizUsername=request.user,quizTitle=tit).first()
            if userScore is not None:
                userplay = "True"
            else:
                userplay = "False"
            user_play.append(userplay)
        else:
            user_play = "False"
    alltitle = zip(title,user_play,noOfQues)
    if title.count() == 0:
        return HttpResponse("404 Page not found")
    return render(request,'quiz/quizCategory.html',{"titles":alltitle,"language":slug})

# def viewTitleScore(request,slug):
#     if request.user.is_authenticated:
#         userScore = UserScore.objects.filter(quizUsername=request.user,quizTitle=slug)
#         if userScore.count() != 0:
#             context = {"userscore":userScore}
#         else:
#             context = {"notPlay":True}
#         return render(request,'quiz/UserScore.html',context)

def quizTitleScore(request,slug):
    title = Title.objects.filter(title=slug).first()
    userscore = UserScore.objects.filter(quizTitle=title,quizUsername=request.user).first()
    if userscore is not None:
            isNotUser = False
            context = {"title":userscore.quizTitle,"user_score":userscore.user_score,"total_score":userscore.total_score,"unanswered":userscore.total_unanswered,"time":userscore.time_consume,"id":userscore.id,"notGiveFeedback":True}
    else:
        isNotUser = True
        context = {"isNotUser":isNotUser}
    return render(request,'quiz/quizResult.html',context)
    
def feedback(request):
    if request.method == 'POST':
        title = request.POST['quizTitle']
        context = {"quizTitle":title}
        return render(request,'quiz/quizFeedback.html',context)

def feedbackHandle(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST['email']
        star = request.POST['star']
        review = request.POST['review']
        title = request.POST['quizTitle']
        quizTitle = Title.objects.filter(title=title).first()
        feedback = Feedback(email=email,stars=star,review=review,quizTitle=quizTitle)
        feedback.save()
        messages.success(request,"Thankyou for your Feedback!!")
        
        return redirect('startQuiz')

def leaderboard(request):
    result = LeaderBoard.objects.all().order_by('-current_score')[:50]
    context = {"result":result}
    return render(request,'quiz/leaderboard.html',context)


def pie_chart(request):
    labels = []
    data = []

    querySet = LeaderBoard.objects.all().order_by('-current_score')[:5]
    for elem in querySet:
        labels.append(elem.user.username)
        data.append(elem.current_score)
    
    return render(request,'chart/pie_chart.html',{
        'labels':labels,
        'data':data
    })
