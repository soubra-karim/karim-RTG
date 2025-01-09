
from django.contrib import admin
from django.urls import path, include
from .views import SignUpView, LoginView, LogoutView, UpdatePasswordView, UpdateEmailView,DisplayResumeInfo,UpdateResumeInfo, UpdateJobPosting, stats_view
urlpatterns = [
    path('Signup/', SignUpView.as_view(), name='Signup'),
    path('Login/', LoginView.as_view(), name='Login'),
    path('Logout/', LogoutView.as_view(), name = 'Logout'),
    path('update-email/', UpdateEmailView.as_view(), name = 'update-email'),
    path('update-password/', UpdatePasswordView.as_view(), name = 'update-password'),
    path('display-resume/',DisplayResumeInfo.as_view(),name='display-resume'),
    path('update-resume/',UpdateResumeInfo.as_view(),name='update-resume'),
    path('edit-job/',UpdateJobPosting.as_view(),name='edit-job'), 
    path('stats_view/',stats_view,name='stats_view'),
]
