from django.urls import path
from account import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('validate_registration/',views.validate_registration,name="validate_registration"),
    path('login/',views.userLogin,name="userLogin"),
    path('validate_login/',views.validate_login,name="validate_login"),
    path('logout/',views.userLogout,name="userLogout"),
    path('changePass/',views.changePass,name="changePass"),
    path('validate_change_password/',views.validate_change_password,name="validate_change_password"),
   
   #reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]