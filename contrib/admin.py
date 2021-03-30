from django.contrib import admin
from . models import userLanguage,userQues,userSnippetLanguage,userSnip
# Register your models here.

class userQuesInline(admin.TabularInline):
    model = userQues

class userSnipInline(admin.TabularInline):
    model = userSnip

class userLanguageAdmin(admin.ModelAdmin):
    list_display = ('userName','language','quesCount')
    list_filter = ('userName','language')
    search_fields = ('language','userName__username')
    list_per_page = 20
    inlines = [
        userQuesInline,
    ]

class userSnippetLanguageAdmin(admin.ModelAdmin):
    list_display = ('userName','language','snippetCount')
    list_filter = ('userName','language')
    search_fields = ('language','userName__username')
    list_per_page = 20
    inlines = [
        userSnipInline,
    ]

class userQuesAdmin(admin.ModelAdmin):
    list_display = ('userLang','Ques','choice1','choice2','choice3','choice4','Ans','updated')
    list_filter = ('userLang','Ques','updated')
    search_fields = ('userLang','Ques','choice1','choice2','choice3','choice4','Ans')
    list_per_page = 20

class userSnipAdmin(admin.ModelAdmin):
    list_display = ('userLang','title','code','summary','updated')
    list_filter = ('userLang','title','updated')
    search_fields = ('userLang','title','code','summary')
    list_per_page = 20

admin.site.register(userLanguage,userLanguageAdmin)
admin.site.register(userSnippetLanguage,userSnippetLanguageAdmin)

admin.site.register(userQues,userQuesAdmin)
admin.site.register(userSnip,userSnipAdmin)
