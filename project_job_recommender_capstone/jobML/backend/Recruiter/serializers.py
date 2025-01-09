from rest_framework import serializers
from UserAuth.models import JobPosting,  ListOfSkills
from rest_framework import serializers
from UserAuth.models import JobPosting
from django.db import transaction
from rest_framework import serializers
from UserAuth.models import User, Resume, Education, WorkExperience, ResumeToSkills

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfSkills
        fields = ('skill_name') 

class JobPostingCreateSerializer(serializers.ModelSerializer):
    job_skills = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    
    class Meta:
        model = JobPosting
        fields = (
            'title',
            'company_name',
            'location',
            'job_description',
            'posted_date',
            'application_deadline',
            'experience_required',
            'job_skills', 
            'benefits',
            'employment_type',
        )
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['user']  
        skills_data = validated_data.pop('job_skills', [])
        
        with transaction.atomic():
            job_posting = JobPosting.objects.create(user=user, **validated_data)

            for skill_name in skills_data:
                skill, created = ListOfSkills.objects.get_or_create(skill_name=skill_name)
                job_posting.skills.add(skill)
        
        return job_posting

    def to_representation(self, instance):
        representation = super(JobPostingCreateSerializer, self).to_representation(instance)
        representation['job_skills'] = [skill.skill_name for skill in instance.skills.all()]
        return representation




class JobPostingSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = JobPosting
        fields = (
            'jobID', 'title', 'company_name', 'location', 'job_description', 
            'posted_date', 'application_deadline', 'requirements', 
            'job_skills', 'benefits', 'employment_type'
        )

class ResumeToSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeToSkills
        fields = ['skill_name']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['school_name', 'degree', 'start_date', 'end_date', 'gpa']

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'job_description']

class ResumeSerializer(serializers.ModelSerializer):
    resume_skills = ResumeToSkillsSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ['resume_skills', 'educations', 'work_experiences']

class UserSerializer(serializers.ModelSerializer):
    resumes = ResumeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'phone_number', 'user_type', 'resumes']