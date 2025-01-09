from django.contrib import admin
from django.urls import path, include
from .views import JobPostingListView, JobPostingCreateView, search_applicants, sendRecommendationsToFrontEnd, display_user_info, update_feedback, liked_applicants, sendEmailtoApplicant


urlpatterns = [
    path('jobPostingListView/', JobPostingListView.as_view(), name='jobPostingListView'),
    path('jobPostingCreateView/', JobPostingCreateView.as_view(), name='jobPostingCreateView'),
    path('search_applicants/', search_applicants, name='search_applicants'),
    path('candidate-recommendations/', sendRecommendationsToFrontEnd, name='candidate-recommendations'),
    path('display_user_info/', display_user_info, name='display_user_info'),
    path('update_feedback/', update_feedback, name='update_feedback'),
    path('liked_applicants/', liked_applicants, name='liked_applicants'), 
    path('send_email_to_applicant/', sendEmailtoApplicant, name='send_email_to_applicant'),
]
