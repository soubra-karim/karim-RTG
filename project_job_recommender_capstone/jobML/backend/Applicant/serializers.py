# serializers.py
from rest_framework import serializers
from UserAuth.models import Resume, Education, WorkExperience, ListOfSkills, ResumeToSkills



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfSkills
        fields = ('skill_name')  

class ResumeToSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeToSkills
        exclude = ('resume',) 

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('resume',) 

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        exclude = ('resume',) 

class ResumeSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True)
    work_experiences = WorkExperienceSerializer(many=True)
    resume_skills = ResumeToSkillsSerializer(many=True)  # Add this line
    class Meta:
        model = Resume
        fields = ('user', 'educations', 'work_experiences', 'resume_skills')  
        read_only_fields = ('user',)  

    def create(self, validated_data):
            educations_data = validated_data.pop('educations', None)
            work_experiences_data = validated_data.pop('work_experiences', None)
            skills_data = validated_data.pop('resume_skills', None)
            print("Skills data:", skills_data)
            user = self.context['user']  
            resume = Resume.objects.create(user=user)
            
            if educations_data:
                for education_data in educations_data:
                    Education.objects.create(resume=resume, **education_data)
            
            if work_experiences_data:
                for work_experience_data in work_experiences_data:
                    WorkExperience.objects.create(resume=resume, **work_experience_data)
            
            if skills_data:
                for skill_dict in skills_data:
                    skill_name = skill_dict['skill_name']
                    if not skill_name:
                        print("Missing 'skill_name' in:", skill_dict)
                        continue
                    skill_instance, _ = ListOfSkills.objects.get_or_create(skill_name=skill_name)
                    ResumeToSkills.objects.create(resume=resume, skill_name=skill_instance)

                return resume
    