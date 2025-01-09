from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from Applicant.serializers import ResumeSerializer
from rest_framework.permissions import IsAuthenticated
from UserAuth.models import Resume
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from coreApp.ResumeScraper.resume import ResumeExtractor
import logging, json
from django.contrib.postgres.aggregates import ArrayAgg
import jwt,os
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from django.core import serializers
from UserAuth.models import Resume,JobPosting,ListOfSkills,FeedbackforJob, ModelVersion
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from Applicant.recommendations import give_suggestions, update_user_feedback
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.http import HttpResponse
from Recruiter.ML_model_resume import MODEL_VERSION
import numpy as np

def getUserFromRequest(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    token = auth_header.split(" ")[1]
    decoded_token = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=["HS256"])
    user_id = decoded_token['id']
    user = get_user_model().objects.get(id=user_id)
    return user

class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        file_path = default_storage.save('uploads/' + file_obj.name, file_obj)
        full_file_path = default_storage.path(file_path)

        
        # scraped_data = scrape_resume_data(full_file_path)  # This needs to be implemented
        extractor = ResumeExtractor()
        scraped_data = extractor.extract_all(filename=full_file_path)
        print(scraped_data)
        return Response(scraped_data, status=status.HTTP_200_OK)

logger = logging.getLogger(__name__)

class ResumeCreateView(APIView):

    def post(self, request, *args, **kwargs):
        user = getUserFromRequest(request=request)
        print(request.data)
        model_version_str = str(MODEL_VERSION)
        serializer = ResumeSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            ModelVersion.objects.update_or_create(
                user_id=user.id,
                defaults={
                    'latest_version': model_version_str  
                })
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log the errors
            logger.error("ResumeCreateView: Validation failed with errors: %s", serializer.errors)
            
            # Respond with the error details
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt
def sendRecommendationsToFrontEnd(request):
    user = getUserFromRequest(request)
    ModelVersionEntry = ModelVersion.objects.get(user=user)
    userModel = ModelVersionEntry.model_version
    latestModel = ModelVersionEntry.latest_version
    print("Getting recommendations")
    if userModel != latestModel:
        recommended_jobs(request)
    return get_recommendations(request)

def recommended_jobs(request):
    print("Generating recommendations")
    job_ids = []
    user = getUserFromRequest(request=request)
    try:
        user_resume = Resume.objects.get(user=user)
        user_skills = user_resume.resume_skills.all()
        user_skills_texts = [skill.skill_name for skill in user_skills]
        latest_work_experience = user_resume.work_experiences.first()
        if latest_work_experience:
            user_title = latest_work_experience.job_title
            user_job_desc = latest_work_experience.job_description
        else:
            user_title = None
            user_job_desc = None
        suggestions_list = give_suggestions(user.id, user_title, user_job_desc,' '.join(user_skills_texts))
        print(f"suggestions_list: {suggestions_list}")
        for suggestion in suggestions_list:
            job_ids.append(suggestion['job_id'])

        jobs_query_set = JobPosting.objects.filter(id__in=job_ids)
        jobs_list = list(jobs_query_set)
        print(jobs_list)
        jobs_ordered = sorted(jobs_list, key=lambda job: job_ids.index(job.id))

        serialized_jobs = serializers.serialize('json', jobs_ordered)
        print(f"seriazlied jobs: {serialized_jobs}")
        return JsonResponse({"recommended_jobs": serialized_jobs})     
    except Resume.DoesNotExist:
        return JsonResponse({"error": "User does not have a resume"}, status=400)

@csrf_exempt
def update_feedback(request):
    try:
        data = json.loads(request.body)
        user = getUserFromRequest(request=request)
        
        job_id = data.get('job_id')
        feedback = data.get('feedback')
        
        update_user_feedback(user_id=user.id, job_id=job_id, feedback=int(feedback))

        return JsonResponse({"message": "Feedback updated successfully"}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# def get_recommendations(request):
#     from Applicant.recommendations import top_recommendations
#     user = getUserFromRequest(request=request)
#     try:
#         top_entries = top_recommendations(user_id=user.id)
#         job_ids = [suggestion['job_id'] for suggestion in top_entries]
#         jobs = JobPosting.objects.filter(id__in=job_ids)
#         job_mapping = {job.id: job for job in jobs}
#         ordered_jobs = [job_mapping[job_id] for job_id in job_ids if job_id in job_mapping]
        
#         serialized_jobs = serializers.serialize('json', ordered_jobs)
#         return JsonResponse({"recommended_jobs": serialized_jobs})
#     except Resume.DoesNotExist:
#         return JsonResponse({"error": "user couldnt be found"}, status=400)
# def get_recommendations(request):
#     from django.core import serializers
#     from django.http import JsonResponse
#     from UserAuth.models import JobPosting, FeedbackforJob  # Assuming FeedbackforJob is the correct model name
#     from Applicant.recommendations import top_recommendations
#     # Assuming getUserFromRequest is a function that extracts a user object from the request

#     user = getUserFromRequest(request=request)
#     try:
#         top_entries = top_recommendations(user_id=user.id)
#         job_ids_scores = {suggestion['job_id']: suggestion['score'] for suggestion in top_entries}
#         jobs = JobPosting.objects.filter(id__in=job_ids_scores.keys())
#         job_mapping = {job.id: job for job in jobs}
#         ordered_jobs_with_scores = []
#         for job_id, score in job_ids_scores.items():
#             if job_id in job_mapping:
#                 job = job_mapping[job_id]
#                 job_data = serializers.serialize('python', [job])[0]  # Serialize to Python native data structure
#                 job_data['fields']['score'] = score  # Adding the score to the job data
#                 ordered_jobs_with_scores.append(job_data)

#         # If you need the result in JSON string format
#         serialized_jobs_with_scores = json.dumps(ordered_jobs_with_scores)  # Convert the list of dictionaries to a JSON string

#         return JsonResponse({"recommended_jobs": serialized_jobs_with_scores})
#     except Resume.DoesNotExist:
#         return JsonResponse({"error": "user couldn't be found"}, status=400)
def get_recommendations(request):
    from Applicant.recommendations import top_recommendations
    user = getUserFromRequest(request=request)
    try:
        top_entries = top_recommendations(user_id=user.id)
        job_ids_scores = {suggestion['job_id']: suggestion['score'] for suggestion in top_entries}
        jobs = JobPosting.objects.filter(id__in=job_ids_scores.keys())
        job_mapping = {job.id: job for job in jobs}
        
        ordered_jobs_with_scores = []
        for job_id, score in job_ids_scores.items():
            if job_id in job_mapping:
                job = job_mapping[job_id]
                job_data = {
                    "id": job.id,
                    "title": job.title,
                    "job_description": job.job_description,
                    "company" : job.company_name,
                    "location": job.location,
                    "score": round((np.log(1 + np.clip(float(score), 0, 100)) * 100) / np.log(101),2),  # Adding the score
                }
                ordered_jobs_with_scores.append(job_data)
        ordered_jobs_with_scores.sort(key=lambda x: x['score'], reverse=True)

        print(ordered_jobs_with_scores)

        return JsonResponse({"recommended_jobs": ordered_jobs_with_scores})
    except Resume.DoesNotExist:
        return JsonResponse({"error": "user couldn't be found"}, status=400)
@csrf_exempt
def search_jobs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('q', '')
    else:
        query = request.GET.get('q', '')

    print(query)
    if query:
        jobs = JobPosting.objects.filter(
            Q(title__icontains=query) | 
            Q(company_name__icontains=query) | 
            Q(location__icontains=query) | 
            Q(job_description__icontains=query),
            application_deadline__gte=timezone.now()
        )
    else:
        jobs = JobPosting.objects.all()

    jobs_list = list(jobs.values(
        'id', 'title', 'company_name', 'location', 'job_description', 'posted_date', 
        'application_deadline', 'experience_required'
    ))
    print(jobs_list)
    return JsonResponse({'jobs': jobs_list})

@csrf_exempt
def get_jobposting(request):
    if request.method =='POST':
        data = json.loads(request.body)
        print(data)
        query = data.get('job_id',None)
    else:
        query = request.get('job_id',None)
    
    if query is None:
        return JsonResponse({"error": "no query found"}, status=400)
    else:
        job = JobPosting.objects.filter(
            Q(id=query)
        ).first()
        job_skills = JobPosting.objects.filter(
            Q(id=query)
        ).prefetch_related('skills').all()
        skill_lists = []
        for skill in job_skills:
            skills = list(skill.skills.all().values_list('skill_name'))

            for sk in skills:
                try:
                    if sk[0][0]==' ':

                        skill_lists.append(sk[0][1:])
                    else:
                        skill_lists.append(sk[0])
                except:
                    skill_lists.append(sk[0])

        print("printing skills")
        print(skill_lists)
        job_result = {'title' : job.title,
                      'company_name' : job.company_name,
                      'location' : job.location,
                      'description' : job.job_description,
                      'posted_date' : job.posted_date,
                      'application_deadline' : job.application_deadline,
                      'employment_type' : job.employment_type,
                      'skills' : skill_lists,
                      'experience_required': job.experience_required}
        print(f"sending data")
        print(job_result)
        return JsonResponse({'job_post': job_result})


def liked_jobs(request):
    user = getUserFromRequest(request=request)
    liked_jobs = FeedbackforJob.objects.filter(user_id=user.id, feedback='1')
    
    job_ids = []
    
    for job in liked_jobs:
        job_ids.append(job.job_posting_id)
    
    if job_ids:
        jobs = JobPosting.objects.filter(id__in=job_ids)
    else:
        jobs = JobPosting.objects.none()
    
    jobs_list = list(jobs.values(
        'id', 'title', 'company_name', 'location', 'job_description', 'posted_date', 
        'application_deadline', 'experience_required'
    ))
    print(jobs_list)
    return JsonResponse({'jobs': jobs_list}, safe=False)

@csrf_exempt
def sendEmailtoRecruiter(request):
    data = json.loads(request.body)
    user = getUserFromRequest(request=request) 
    job_id = data.get('job_id')
    job_posting = JobPosting.objects.get(id=job_id)
    subject = f'{user.name} has applied to your Job Posting: {job_posting.title}'
    message = f"This is a message regarding your job posting titled {job_posting.title}. {user.name} has applied to this position. To reach the applicant to further the process, the following contact information is available \n Phone Number: {user.phone_number} \n Email Address: {user.email} \n\n Regards,\n JobSync Team "
    from_email = 'jobsynccanada@gmail.com'  
    

    if job_posting.user == None:
        return HttpResponse("Email sent successfully.")
    else:
        recipient_email = job_posting.user.email

    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponse("Email sent successfully.")

