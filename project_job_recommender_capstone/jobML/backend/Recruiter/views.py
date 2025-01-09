from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from UserAuth.models import JobPosting
from .serializers import JobPostingSerializer, JobPostingCreateSerializer
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.db.models import Q
from UserAuth.models import User, Resume, ResumeToSkills, Education, WorkExperience, Project, ModelVersionResume, FeedbackforResume
from django.contrib.auth import get_user_model
import jwt,os
from django.core.serializers import serialize
from django.core import serializers
from Recruiter.recommendations_resume import give_suggestions, update_user_feedback
from Recruiter.ML_model_resume import MODEL_VERSION
from .serializers import UserSerializer
import traceback
from collections import defaultdict
from django.core.mail import send_mail
from django.http import HttpResponse


def getUserFromRequest(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    token = auth_header.split(" ")[1]
    decoded_token = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=["HS256"])
    user_id = decoded_token['id']
    user = get_user_model().objects.get(id=user_id)
    return user

class JobPostingListView(APIView):
    # permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        user = getUserFromRequest(request=request)
        print(user)
        job_postings = JobPosting.objects.filter(user_id=user.id)

        job_postings_list = []
        for job in job_postings:
            job_postings_list.append({
                'id': job.id,
                'title': job.title,
                'company_name': job.company_name,
                'location': job.location,
                'job_description': job.job_description,
                'posted_date': job.posted_date,
                'application_deadline': job.application_deadline,
                'experience_required': job.experience_required,
                'benefits': job.benefits,
                'employment_type': job.employment_type,
                'skills': [skill.skill_name for skill in job.skills.all()]
            })
        return Response({'jobs': job_postings_list}, status=status.HTTP_200_OK)

class JobPostingCreateView(APIView):
    # permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        user = getUserFromRequest(request=request)
        model_version_str = str(MODEL_VERSION)
        serializer = JobPostingCreateSerializer(data=request.data,  context={'request': request, 'user': user})
        if serializer.is_valid():
            job = serializer.save()
            ModelVersionResume.objects.update_or_create(
                job_posting_id=job.id,
                defaults={
                    'latest_version': model_version_str  
                })
            job.skill_list_save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Errors:", serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt  
def search_applicants(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('q', '')
    else:
        query = request.GET.get('q', '')

    if query:
        applicants = User.objects.filter(
            Q(user_type=User.UserType.APPLICANT) & (
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(resumes__resume_skills__skill_name__icontains=query) |
                Q(resumes__educations__school_name__icontains=query) |
                Q(resumes__work_experiences__company_name__icontains=query) |
                Q(resumes__projects__title__icontains=query)
            )
        ).distinct().prefetch_related('resumes__resume_skills', 'resumes__educations', 'resumes__work_experiences', 'resumes__projects')
    else:
        applicants = User.objects.filter(user_type=User.UserType.APPLICANT).prefetch_related('resumes__resume_skills', 'resumes__educations', 'resumes__work_experiences', 'resumes__projects')

    applicants_list = []
    for applicant in applicants:
        applicant_dict = {
            'id': applicant.id,
            'name': applicant.name,
            'email': applicant.email,
            'phone_number': applicant.phone_number,
            'skills': [],
            'educations': [],
            'work_experiences': [],
            'projects': []
        }
        
        resume = applicant.resumes.first()
        if resume:
            applicant_dict['skills'] = list(resume.resume_skills.values('skill_name'))
            applicant_dict['educations'] = list(resume.educations.values('school_name', 'degree', 'start_date', 'end_date', 'gpa'))
            applicant_dict['work_experiences'] = list(resume.work_experiences.values('company_name', 'job_title', 'start_date', 'end_date', 'job_description'))
            applicant_dict['projects'] = list(resume.projects.values('title', 'description'))

        applicants_list.append(applicant_dict)

    return JsonResponse({'applicants': applicants_list})

class UploadJob:

    def upload(self,data):
        print("HERE")
        serialzer=JobPostingCreateSerializer(data=data)

        if serialzer.is_valid():
            serialzer.save()
            return True
        else:
            return False
@csrf_exempt        
def sendRecommendationsToFrontEnd(request):
    print(request.body)
    data = json.loads(request.body)
    job_id = data['job_id']
    user = getUserFromRequest(request)
    ModelVersionEntry = ModelVersionResume.objects.get(job_posting_id=job_id)
    resumeModel = ModelVersionEntry.model_version
    latestModel = ModelVersionEntry.latest_version
    print("Getting recommendations")
    if resumeModel != latestModel:
        recommended_jobs(request)
    return get_recommendations(request) 

def recommended_jobs(request):
    print("Generating recommendations")
    user_ids = []
    user = getUserFromRequest(request=request)
    data = json.loads(request.body)
    job_id = data['job_id']
    job_posting = JobPosting.objects.get(id=job_id)
    print(job_posting)
    try:
        job_skills = job_posting.skills.all()
        job_skills_texts = [skill.skill_name for skill in job_skills]
        job_title = job_posting.title
        job_desc = job_posting.job_description

        suggestions_list = give_suggestions(job_posting.id, job_title, job_desc,' '.join(job_skills_texts))
        print(f"suggestions_list: {suggestions_list}")
        print(f"Inital recommendations complete")
        
        return JsonResponse({"success": "recommended_jobs"})   
    except Resume.DoesNotExist:
        return JsonResponse({"error": "User does not have a resume"}, status=400)

@csrf_exempt
def update_feedback(request):
    try:
        data = json.loads(request.body)
        print(data)
        #user = getUserFromRequest(request=request)
        user_id = data['user_id']
        job_id = data['job_id']
        feedback = data['feedback']
        
        update_user_feedback(user_id=user_id, job_id=job_id, feedback=int(feedback))

        return JsonResponse({"message": "Feedback updated successfully"}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

def get_recommendations(request):
    from Recruiter.recommendations_resume import top_recommendations
    data = json.loads(request.body)
    job_id = data['job_id']
    try:
        top_entries = top_recommendations(job_id=job_id)
        print(top_entries)
        user_ids_scores = {suggestion['user_id']: suggestion['score'] for suggestion in top_entries}
        users = User.objects.filter(id__in=user_ids_scores.keys())
        
        user_mapping = {user.id: user for user in users}
        
        ordered_users_with_scores = []
        for user_id, score in user_ids_scores.items():
            if user_id in user_mapping:
                user = user_mapping[user_id]
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "score": float(score), 
                }
                ordered_users_with_scores.append(user_data)
        ordered_users_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return JsonResponse({"recommended_users": ordered_users_with_scores})
    except User.DoesNotExist: 
        return JsonResponse({"error": "user couldn't be found"}, status=400)
    

@csrf_exempt
def display_user_info(request):
    try:
        data = json.loads(request.body)
        user_id = data['user_id']
        user = User.objects.get(id=user_id)

        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number,
            'skills': [],
            'educations': [],
            'work_experiences': [],
            'projects': []
        }

        resume = user.resumes.first()  
        if resume:
            user_data['skills'] = list(resume.resume_skills.values('skill_name'))
            user_data['educations'] = list(resume.educations.values('school_name', 'degree', 'start_date', 'end_date', 'gpa'))
            user_data['work_experiences'] = list(resume.work_experiences.values('company_name', 'job_title', 'start_date', 'end_date', 'job_description'))
            user_data['projects'] = list(resume.projects.values('title', 'description')) if hasattr(resume, 'projects') else []

        return JsonResponse(user_data)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def liked_applicants(request):
    user = getUserFromRequest(request=request)
    user_jobs = JobPosting.objects.filter(user_id=user.id)

    liked_feedbacks = FeedbackforResume.objects.filter(
        job_posting__in=user_jobs,
        feedback='1'
    ).prefetch_related('user', 'job_posting').distinct()

    jobs_with_applicants = defaultdict(list)
    for feedback in liked_feedbacks:
        if feedback.user and feedback.job_posting:
            applicant_dict = {
                'id': feedback.user.id,
                'name': feedback.user.name,
                'email': feedback.user.email,
                'phone_number': feedback.user.phone_number,
                'skills': [],
                'educations': [],
                'work_experiences': [],
                'projects': []
            }

            resume = feedback.user.resumes.first()
            if resume:
                applicant_dict['skills'] = list(resume.resume_skills.values('skill_name'))
                applicant_dict['educations'] = list(resume.educations.values('school_name', 'degree', 'start_date', 'end_date', 'gpa'))
                applicant_dict['work_experiences'] = list(resume.work_experiences.values('company_name', 'job_title', 'start_date', 'end_date', 'job_description'))
                applicant_dict['projects'] = list(resume.projects.values('title', 'description'))

            jobs_with_applicants[feedback.job_posting.title].append(applicant_dict)

    jobs_with_applicants = dict(jobs_with_applicants)

    return JsonResponse({'applicants': jobs_with_applicants})

@csrf_exempt
def sendEmailtoApplicant(request):
    data = json.loads(request.body)
    user = getUserFromRequest(request=request) 
    job_id = data.get('job_id')
    job_posting = JobPosting.objects.get(id=job_id)
    applicant_id = data.get('applicant_id')
    applicant = User.objects.get(id=applicant_id)
    recipient_email = applicant.email

    subject = f'{job_posting.company_name} is reaching out to you regarding their opening {job_posting.title}'
    message = f"This is a message regarding  job posting titled {job_posting.title}. {job_posting.company_name} would like tointerview you. Please reply to the following email address with your availability next week. \n Email Address: {user.email} \n Regards,\n JobSync Team "
    from_email = 'jobsynccanada@gmail.com'  
    recipient_list = [recipient_email]
    print(recipient_list)
    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse("Email sent successfully.")