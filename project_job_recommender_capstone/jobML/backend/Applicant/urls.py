from django.contrib import admin
from django.urls import path, include
from .views import ResumeCreateView, ResumeUploadView, search_jobs, recommended_jobs, update_feedback, sendRecommendationsToFrontEnd
from .views import get_recommendations, liked_jobs,get_jobposting,sendEmailtoRecruiter


urlpatterns = [
    path('upload-resume/', ResumeUploadView.as_view(), name='upload-resume'),
    path('create-resume/', ResumeCreateView.as_view(), name='create-resume'),
    path('search_jobs/', search_jobs, name='search_jobs'),
    path('recommend-jobs/', recommended_jobs, name='recommend-jobs'),
    path('send-recommendations/', sendRecommendationsToFrontEnd, name='send-recommendations'),
    path('get-recommendations/', get_recommendations, name='get-recommendations'),
    path('update_feedback/', update_feedback, name='update_feedback'),
    path('liked_jobs/', liked_jobs, name='liked_jobs'),
    path('get_jobpost/',get_jobposting, name='get_jobpost'),
    path('send_email_to_recruiter/',sendEmailtoRecruiter, name='send_email_to_recruiter')
]
