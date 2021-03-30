from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class userLanguage(models.Model):
    userName = models.ForeignKey(User,on_delete=models.CASCADE)
    language = models.CharField(max_length=100,primary_key=True)
    quesCount = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.userName.username) + " (" + self.language + ") " + str(self.quesCount)

class userSnippetLanguage(models.Model):
    userName = models.ForeignKey(User,on_delete=models.CASCADE)
    language = models.CharField(max_length=100,primary_key=True)
    snippetCount = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.userName.username) + " (" + self.language + ") " + str(self.snippetCount)

class userQues(models.Model):
    userLang = models.ForeignKey(userLanguage,on_delete=models.CASCADE)
    Ques = models.CharField(max_length=200)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    Ans = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Ques +"  "+ str(self.userLang)
    
class userSnip(models.Model):
    userLang = models.ForeignKey(userSnippetLanguage,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    code = models.TextField()
    summary = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " " + str(self.userLang)