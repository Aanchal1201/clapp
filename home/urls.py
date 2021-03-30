from django.urls import path
from home import views

urlpatterns = [
    path('',views.home,name="home"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('viewProfile/',views.viewProfile,name="viewProfile"),
    path('editUserProfile/',views.editUserProfile,name="editUserProfile"),
    path('handleEditProfile/',views.handleEditProfile,name="handleEditProfile"),
    path('privacyPolicy/',views.privacyPolicy,name="privacyPolicy"),
    path('termsconditions/',views.termsconditions,name="termsconditions"),
    path('faqs/',views.faqs,name="faqs"),
    path('userDashboard/',views.userDashboard,name="userDashboard"),
]