from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    class UserType(models.TextChoices):
        RECRUITER = 'Recruiter', ('Recruiter')
        APPLICANT = 'Applicant', ('Applicant')

    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    user_type = models.CharField(
        max_length=50,
        choices=UserType.choices,
        default=UserType.APPLICANT,
    )

    #Was getting error with permissions, this fixes it do not change
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="userauth_user_set",  
        related_query_name="userauth_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="userauth_permission_set", 
        related_query_name="userauth_user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class Resume(models.Model):
    #resumeID = models.CharField(max_length=255, unique=True, default='DefaultResumeID')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resumes')

class Education(models.Model):
    #educationID = models.CharField(max_length=255, unique=True, default='DefaultEduID')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    school_name = models.CharField(max_length=200, default='Default School')
    degree = models.CharField(max_length=200, default='Default Degree')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    gpa = models.FloatField(max_length=100, blank=True, null=True, default=0.0)

class WorkExperience(models.Model):
   # experienceID = models.CharField(max_length=255, unique=True, default='DefaultExpID')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=200, default='Default Company')
    job_title = models.CharField(max_length=200, default='Default Job Title')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    job_description = models.TextField(default='Default Description')

class ResumeToSkills(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='resume_skills')
    skill_name = models.CharField(max_length=255, default='DefaultSkillID')

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200, default='Default Project Title')
    description = models.TextField(default='Default Project Description')

class ListOfSkills(models.Model):
    
    skill_name = models.CharField(max_length=200, default='Default Skill')

    def __str__(self):
        return self.skill_name

class JobPosting(models.Model):
    #jobID = models.AutoField(max_length=255, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    posted_date = models.DateField(default=timezone.now)
    application_deadline = models.DateField(default=timezone.now)
    experience_required = models.CharField(max_length=255, null=True, blank=True, default='No experience required')  
    benefits = models.TextField(max_length=700, null=True, blank=True)
    employment_type = models.CharField(max_length=200, null=True, blank=True)
    skills = models.ManyToManyField(ListOfSkills, related_name='job_postings', blank=True)  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator')

    skills_list = models.JSONField(default=list)

    cluster = models.IntegerField(max_length=255, default=0)


    def skill_list_save(self, *args, **kwargs):
        self.skills_list = list(self.skills.values_list('skill_name', flat=True))
        super().save(*args, **kwargs)

    

    def __str__(self):
        return self.title

class JobToClusters(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='job_cluster')
    cluster = models.CharField(max_length=255, default='defaultcluster')

class FeedbackforJob(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')
    feedback = models.CharField(max_length=255, default='0')
    score = models.CharField(max_length=255, default='0')

class ModelVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='model_version')
    model_version = models.CharField(max_length=255, default='0')
    latest_version = models.CharField(max_length=255, default='0')

class ResumetoClusters(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resume_cluster')
    cluster = models.CharField(max_length=255, default='defaultcluster')

class ModelVersionResume(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.SET_NULL,null=True, blank=True, related_name='model_version_resume')
    model_version = models.CharField(max_length=255, default='0')
    latest_version = models.CharField(max_length=255, default='0')

class FeedbackforResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_resume')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_resume')
    feedback = models.CharField(max_length=255, default='0')
    score = models.CharField(max_length=255, default='0')