import pandas as pd
from pathlib import Path
from django.conf import settings
import django
import os
from ResumeScraper.resume import ResumeExtractor
from django.db.models import Q



import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parent.parent.__str__())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()

# from ...backend.Recruiter.viewsimport import UploadJob
from UserAuth.models import JobPosting, ListOfSkills
from django.utils import timezone
from Recruiter.views import UploadJob
import os

from django.core.wsgi import get_wsgi_application





csvpath = Path(__file__).parent / 'dice_com-job_us_sample.csv'
jobs_df = pd.read_csv(csvpath)

jobs_df = jobs_df.drop(["advertiserurl","jobid","postdate","shift","site_name","uniq_id"],axis=1)

print(jobs_df.head())
print(jobs_df.info())
extract_info = ResumeExtractor()
limit = 1000
count=0
for index,row in jobs_df.iterrows():
        skills_found = extract_info.extract_skills(row['jobdescription']).split(",")
        job_posting_data = {
            "title": row['jobtitle'],
            "company_name": row['company'],
            "location": row['joblocation_address'],
            "job_description": row['jobdescription'],
            "posted_date": timezone.now(),
            "application_deadline": timezone.now() + timezone.timedelta(days=100),
            "experience_required": "N/A",
            "creator": None,
        }
        existing_job_posting = JobPosting.objects.filter(
                Q(title=job_posting_data["title"]) &
                Q(company_name=job_posting_data["company_name"]) &
                Q(location=job_posting_data["location"]) &
                Q(job_description=job_posting_data["job_description"])
                ).first()
        if existing_job_posting is None:
            job_posting = JobPosting.objects.create(**job_posting_data)
            count+=1
            # skills_list = current_job_data.get("skills", [])

            for skill_name in skills_found:
                    skill, created = ListOfSkills.objects.get_or_create(skill_name=skill_name)
                    job_posting.skills.add(skill)
        
        if count>=limit:
               break