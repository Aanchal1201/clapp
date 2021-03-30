from django.urls import path
from contrib import views

urlpatterns = [
    path('',views.contribHome,name="contribHome"),
    path('blog',views.contribBlog,name="contribBlog"),
    path('quiz',views.contribQuiz,name="contribQuiz"),
    path('quiz/<str:lang>',views.quizQues,name="quizQues"),
    path('addLang',views.addLang,name="addLang"),
    path('quiz/<str:lang>/addQues',views.addQues,name="addQues"),
    path('quiz/<str:lang>/deleteQues/<int:id>',views.deleteQues,name="deleteQues"),
    path('quiz/<str:lang>/EditQues/<int:id>',views.EditQues,name="EditQues"),

    path('snippet',views.contribsnippet,name="contribsnippet"),
    path('snippet/<str:lang>',views.snippetLang,name="snippetLang"),
    path('addSnippetLang',views.addSnippetLang,name="addSnippetLang"),
    path('snippet/<str:lang>/addSnip',views.addSnip,name="addSnip"),
    path('snippet/<str:lang>/deleteSnip/<int:id>',views.deleteSnip,name="deleteSnip"),
    path('snippet/<str:lang>/editSnip/<int:id>',views.editSnip,name="editSnip"),
]