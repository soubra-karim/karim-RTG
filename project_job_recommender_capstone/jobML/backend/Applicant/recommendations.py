import re
import sys, os, django
from pathlib import Path

from django.shortcuts import get_object_or_404
import numpy as np
sys.path.append(Path(__file__).resolve().parent.parent.__str__())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()
from UserAuth.models import JobPosting,FeedbackforJob,ModelVersion

from joblib import load
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import warnings; warnings.simplefilter('ignore')
import os
import pandas as pd

def create_clustered_model():
    jobpostings = JobPosting.objects.all()
    jobpostings_list = []
    for jp in jobpostings:
        jobpostings_list.append({
            'id': jp.id,
            'title': jp.title,
            'job_description': jp.job_description,
            'skills': jp.skills_list,
            'cluster_no':jp.cluster
        })
    return jobpostings_list

def feedback_model():
    feedback_entries = FeedbackforJob.objects.select_related('job_posting')
    feedback_list = []
    for feedback in feedback_entries:
        feedback_list.append({
            'feedback': feedback.feedback,
            'job_id': feedback.job_posting.id,
            'user_id': feedback.user.id,
            'job_title': feedback.job_posting.title,  
        })
    return feedback_list

def update_feedback_database(user_id, new_suggestions_list):
    FeedbackforJob.objects.filter(user_id=user_id).delete()

    for entry in new_suggestions_list:
        job_id = entry["job_id"]
        feedback = entry["feedback"]
        score = entry["score"]

        # Create a new feedback entry
        FeedbackforJob.objects.create(
            job_posting_id=job_id,
            user_id=user_id,
            feedback=feedback,
            score=score
        )

def update_model_version_database(user_id, Model_Version):
    model_version_str = str(Model_Version)
    ModelVersion.objects.update_or_create(
            user=user_id,
            defaults={
                'model_version': model_version_str 
            }
        )

def update_user_feedback(user_id, job_id, feedback):
    print(f"--- Changing feedback for user {user_id}, job {job_id} to feedback value {feedback} ---")
    feedback_entry = get_object_or_404(FeedbackforJob, job_posting_id=job_id, user_id=user_id)
    feedback_entry.feedback = feedback
    feedback_entry.save()

def top_recommendations(user_id):
    print("printing user id")
    print(user_id)
    top_feedback_entries = FeedbackforJob.objects.filter(
        user_id = user_id, 
        feedback = 0,
    ).order_by('-score')[:12] 
    top_entries_list = [{'user_id': entry.user_id,'job_id': entry.job_posting_id,"score" : entry.score} for entry in top_feedback_entries]
    return top_entries_list

def clean_text(text):
    # Initial replacements
    replacements = {
        "&nbsp;": " ", "\x92": " ", "\x95": " ", "&amp;": " ",
        "*": " ", ".": "", "co&#39;s": "", "\xae&quot;": "",
        "&#39;s": "", "&quot;": "", "?": "", "@": "",
        "\x96": "", "(": "", ")": "", "+": "",
        "—": "", ":": "", ",": "", "/": " "
    }
    cleaned_text = text
    for old, new in replacements.items():
        cleaned_text = cleaned_text.replace(old, new)
    cleaned_text = cleaned_text.lower()
    cleaned_text = re.sub(r'\d+', '', cleaned_text)  # Remove numbers
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove punctuation
    
    return cleaned_text

def text_scrubber(values):
    result = []
    for item in values:
        if isinstance(item, list) or isinstance(item, np.ndarray):
            temp = ' '.join(item)
            result.append(temp.lower()) 
    return result

def give_suggestions(user_id, user_job_title, user_job_description, user_skills):
    jobs = create_clustered_model()
    df = pd.DataFrame(jobs)

    Model_Version = get_object_or_404(ModelVersion, user_id=user_id)
    Model_Version = Model_Version.latest_version

    # Load your model components
    vec_title = load(f'Applicant/model_settings_ver{Model_Version}/vectorizer_title.joblib')
    vec_desc = load(f'Applicant/model_settings_ver{Model_Version}/vectorizer_description.joblib')
    vec_skills = load(f'Applicant/model_settings_ver{Model_Version}/vectorizer_skills.joblib')
    cluster_lr = load(f'Applicant/model_settings_ver{Model_Version}/cluster_lr.joblib')
    feedback_lr = load(f'Applicant/model_settings_ver{Model_Version}/feedback_lr.joblib')
    comps = load(f'Applicant/model_settings_ver{Model_Version}/comps.joblib')
    comps_indexed = load(f'Applicant/model_settings_ver{Model_Version}/comps_indexed.joblib')

    user_job_description = clean_text(user_job_description)
    # user_skills = text_scrubber(user_skills)

    # Vectorize user's skills and job descriptions
    user_description = pd.DataFrame(vec_desc.transform([user_job_description]).todense())
    user_description.columns = vec_desc.get_feature_names_out()
    user_skills = pd.DataFrame(vec_skills.transform([user_skills]).todense())
    user_skills.columns = vec_skills.get_feature_names_out()
    user_title = pd.DataFrame(vec_title.transform([user_job_title]).todense())
    user_title.columns = vec_title.get_feature_names_out()
    mat = pd.concat([user_title, user_skills, user_description], axis=1) 
    
    user_comps = pd.DataFrame(mat)

    # --------- First Logistics Regression: Predict cluster for user ---------
    predicted_cluster = cluster_lr.predict(user_comps)[0]
    print(f"Users CLUSTER NUMBER: {predicted_cluster}")

    # --------- Cosine Similarity: Find distance of each job to user ---------
    cos_sim = pd.DataFrame(cosine_similarity(user_comps, comps_indexed[comps_indexed.index == predicted_cluster]))

    df['cluster_no'] = pd.to_numeric(df['cluster_no'], errors='coerce')
    samp_for_cluster = df[df['cluster_no'] == predicted_cluster]
    cos_sim = cos_sim.T.set_index(samp_for_cluster['id'])
    cos_sim.columns = ['score']
    top_cos_sim = cos_sim.sort_values('score', ascending=False)[:30]
    
    # --------- Second Logistics Regression: Predicted probability of user liking Job ---------
    top_jobs_features = comps.loc[top_cos_sim.index] 

    probabilities = feedback_lr.predict_proba(top_jobs_features)[:, 1]  # Assuming 1 is the label for 'like'
    
    # Add probabilities to top_cos_sim and sort by it
    top_cos_sim['like_probability'] = probabilities

    # ---------Adding scores ---------
    top_cos_sim['combined_score'] = top_cos_sim['score'] + top_cos_sim['like_probability']

    max_score = top_cos_sim['score'].max()
    min_score = top_cos_sim['score'].min()
    max_like_probability = top_cos_sim['like_probability'].max()
    min_like_probability = top_cos_sim['like_probability'].min()

    top_cos_sim['normalized_score'] = (top_cos_sim['score'] - min_score) / (max_score - min_score)
    top_cos_sim['normalized_like_probability'] = (top_cos_sim['like_probability'] - min_like_probability) / (max_like_probability - min_like_probability)

    alpha = 0.7
    beta = 0.3

    top_cos_sim['confidence_rating'] = alpha * top_cos_sim['normalized_score'] + beta * top_cos_sim['normalized_like_probability']
    top_cos_sim = top_cos_sim.sort_values('confidence_rating', ascending=False)
    
    new_suggestions_list = []
    for job_id, details in top_cos_sim.iterrows():
        job_title = samp_for_cluster[samp_for_cluster['id'] == job_id]['title'].values[0]
        confidence_rating = round(details['confidence_rating'] * 100, 2)
        new_suggestions_list.append({
            "user_id": user_id,
            "job_id": job_id,
            "suggestions": job_title,
            "score": confidence_rating, # Score is now confidence rating!
            "feedback": 0,
        })
    update_feedback_database(user_id, new_suggestions_list)
    update_model_version_database(user_id, Model_Version)
    return new_suggestions_list

# ------------- initial rec -------------
# placeholder
# sel_user_id = 1
# user_skills = "agile, QA"
# user_job_title = "automation test engineer"
# user_job_description = "US Citizens and Green Card Holders and those authorized to work in the US are encouraged to apply. We are unable to sponsor H1b candidates at this timeJob DescriptionWe are seeking a Director of Quality Assurance to be responsible for the overall product quality of all external facing company’s applications.This position will be responsible for leading, driving, designing, and planning the implementation of strategic and operational quality assurance activities for our current customer base of automotive dealers and car rental companies.This person will work closely with Product, Development, and Business Analysts Teams to ensure timely, accurate, and fully tested applications are delivered to our customers that fully meet their business needs.This position will also be responsible for mentoring quality assurance team members and enforcing that proper test planning and execution processes are followed.Skills/Qualifications:Bachelors in Computer Science, Information Systems, or Business AdministrationMinimum 6 years' applicable experience leading and/or directing Software Quality Assurance team(s)Demonstrated consistent leadership effectiveness in technology and business related strategic planning, operations, implementation delivery and overall IT capability (people, process, technology) developmentDemonstrated, proven understanding of both manual and automation testing methodologiesEstablished leadership track record of human capital management principles, practices, and procedures Collect, analyze, and report summarized QA information and trends to President. Guide and train their team to meet and exceed quality standards.Maintain product quality by establishing and enforcing QA policies and proceduresCollaborate with other members of management to develop quality assurance standards for new designs and production methodsMaintain QA staff by recruiting, selecting, orienting, and training employees.Experience with both manual and automation testing using offshore teams"
# print(f"Resume input: {user_skills}, {user_job_title}, {user_job_description}")

# cos_sim_result = give_suggestions(sel_user_id, user_skills, user_job_description, user_job_title)
# print(f"--- Reccomendations: {cos_sim_result} ---")

# ------------- getting top rec -------------
# user_id = 1  # Replace with the actual user_id you want to query
# top_entries = top_recommendations(user_id)
# print(top_entries)

# ------------- updating feedback -------------
# user_id=1
# job_id='836'
# feedback=1
# update_user_feedback(user_id, job_id, feedback)
# user_id=2
# job_id='201'
# feedback=1
# update_user_feedback(user_id, job_id, feedback)
# user_id=2
# job_id='3'
# feedback=1
# update_user_feedback(user_id, job_id, feedback)