from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import mark_safe
# Create your models here.

class Language(models.Model):
    language = models.CharField(max_length=100,primary_key=True)
    
    def __str__(self):
        return self.language

class Title(models.Model):
    LEVEL = (
        ("Easy","Easy"),
        ("Medium","Medium"),
        ("Difficult","Difficult"),
    )
    Language = models.ForeignKey(Language,on_delete=models.CASCADE)
    title = models.CharField(max_length=300,primary_key=True)
    difficulty = models.CharField(choices=LEVEL,max_length=50,default="Easy")
    image = models.ImageField(upload_to='images/Quiz/',blank=True, null=True)
    timeTaken = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="/media/%s" width="80" height="50" />'% (self.image))
    image_tag.short_description = 'ProfileImage'

class Quiz(models.Model):
    title = models.ForeignKey(Title,on_delete=models.CASCADE)
    Ques = models.CharField(max_length=200)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    Ans = models.CharField(max_length=200)
    createdDate = models.DateField(auto_now_add=True)
    modifiedDate = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.Ques

class UserScore(models.Model):
    quizUsername = models.ForeignKey(User,on_delete=models.CASCADE)
    quizTitle = models.ForeignKey(Title,on_delete=models.CASCADE)
    user_score = models.IntegerField()
    total_score = models.IntegerField()
    total_correct = models.IntegerField()
    total_incorrect = models.IntegerField()
    total_unanswered = models.IntegerField()
    time_consume = models.CharField(max_length=50)
    quiz_data = models.TextField()
    played_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.quizUsername) + " " + str(self.quizTitle) + " " + str(self.user_score)
    
class Feedback(models.Model):
    email = models.CharField(max_length=200)
    stars = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    quizTitle = models.ForeignKey(Title,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.email + " " + str(self.stars)

class LeaderBoard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    current_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    