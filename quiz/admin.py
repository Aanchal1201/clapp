from django.contrib import admin
from . models import Language,Title,Quiz,UserScore,Feedback,LeaderBoard
# Register your models here.

class TitleInline(admin.TabularInline):
    model = Title

class QuizInline(admin.TabularInline):
    model = Quiz

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language',)
    list_filter = ('language',)
    inlines = [
        TitleInline,
    ]

class TitleAdmin(admin.ModelAdmin):
    inlines = [
        QuizInline,
    ]
    list_display = ('Language','title','difficulty','timeTaken','created','image_tag')
    list_filter = ('Language','difficulty','created')
    search_fields = ('Language__language','title','difficulty','timeTaken','created')
    list_editable = ('timeTaken',)
    list_display_links = ('Language','title')
   
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title','Ques','Ans','createdDate')
    list_filter = ('title','createdDate')
    search_fields = ('title__title','Ques','choice1','choice2','choice3','choice4','Ans')
    list_per_page = 30

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('quizTitle','email','stars','review')
    list_filter = ('stars','quizTitle')

class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('quizUsername','quizTitle','user_score','total_score','time_consume','played_date')
    list_filter = ('quizTitle','played_date')
    search_fields = ('quizUsername__username','quizTitle__title','time_consume','user_score')

class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ('user','current_score')
    list_filter = ('current_score',)
    list_editable = ('current_score',)

admin.site.register(Language,LanguageAdmin)
admin.site.register(Title,TitleAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(UserScore,UserScoreAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(LeaderBoard,LeaderBoardAdmin)