import re
import sys, os, django
from pathlib import Path

from django.shortcuts import get_object_or_404
sys.path.append(Path(__file__).resolve().parent.parent.__str__())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()
from UserAuth.models import FeedbackforResume,ModelVersionResume,Resume, User

from joblib import load
from sklearn.metrics.pairwise import cosine_similarity
from pylab import rcParams

import pandas as pd
import warnings; warnings.simplefilter('ignore')
import os
import pandas as pd

def create_clustered_model():
    user_resumes = Resume.objects.prefetch_related('work_experiences', 'educations', 'projects', 'resume_skills')
    
    resume_dict = {}
    for resume in user_resumes:
        user_clusters = resume.user.resume_cluster.all() if resume.user else None
        cluster_no = 'No Cluster'
        if user_clusters:
            cluster_no = user_clusters.first().cluster
        if resume.user_id not in resume_dict:
            resume_dict[resume.user_id] = {
                'user_id': resume.user_id if resume.user else None,
                'title': [],
                'job_description': '', 
                'skills': list(resume.resume_skills.values_list('skill_name', flat=True)),
                'cluster_no': cluster_no
            }

        for exp in resume.work_experiences.all():
            if exp.job_title not in resume_dict[resume.user_id]['title']:
                resume_dict[resume.user_id]['title'].append(exp.job_title)
            if not resume_dict[resume.user_id]['job_description']:
                resume_dict[resume.user_id]['job_description'] = exp.job_description

    resume_list = list(resume_dict.values())
    return resume_list

def feedback_model():
    feedback_entries = FeedbackforResume.objects.select_related('job_posting')
    feedback_list = []
    for feedback in feedback_entries:
        feedback_list.append({
            'feedback': feedback.feedback,
            'job_id': feedback.job_posting.id,
            'user_id': feedback.user.id,
            'job_title': feedback.job_posting.title, 
        })
    return feedback_list

def update_feedback_database(job_id, new_suggestions_list):
    FeedbackforResume.objects.filter(job_posting_id=job_id).delete()

    for entry in new_suggestions_list:
        user_id = entry["user_id"]
        feedback = entry["feedback"]
        score = entry["score"]

        FeedbackforResume.objects.create(
            job_posting_id=job_id,
            user_id=user_id,
            feedback=feedback,
            score=score
        )

def update_model_version_database(job_id, Model_Version):
    model_version_str = str(Model_Version)
    ModelVersionResume.objects.update_or_create(
            job_posting_id=job_id,
            defaults={
                'model_version': model_version_str 
            }
        )

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

def update_user_feedback(user_id, job_id, feedback):
    print(f"--- Changing feedback for job {job_id}, user {user_id} to feedback value {feedback} ---")
    feedback_entry = get_object_or_404(FeedbackforResume, job_posting_id=job_id, user_id=user_id)
    feedback_entry.feedback = feedback
    feedback_entry.save()

def top_recommendations(job_id):
    top_feedback_entries = FeedbackforResume.objects.filter(
        job_posting_id = job_id, 
        feedback = 0,
    ).order_by('-score')[:12]  
    top_entries_list = [{'job_id': entry.job_posting_id,'user_id': entry.user_id,"score":entry.score} for entry in top_feedback_entries]
    return top_entries_list

def give_suggestions(job_id, job_title, job_description, job_skills):
    resumes = create_clustered_model()
    df = pd.DataFrame(resumes)

    Model_Version = get_object_or_404(ModelVersionResume, job_posting_id=job_id)
    Model_Version = Model_Version.latest_version

    # Load your model components
    vec_title = load(f'Recruiter/model_settings_ver{Model_Version}/vectorizer_title.joblib')
    vec_desc = load(f'Recruiter/model_settings_ver{Model_Version}/vectorizer_description.joblib')
    vec_skills = load(f'Recruiter/model_settings_ver{Model_Version}/vectorizer_skills.joblib')
    cluster_lr = load(f'Recruiter/model_settings_ver{Model_Version}/cluster_lr.joblib')
    feedback_lr = load(f'Recruiter/model_settings_ver{Model_Version}/feedback_lr.joblib')
    comps = load(f'Recruiter/model_settings_ver{Model_Version}/comps.joblib')
    comps_indexed = load(f'Recruiter/model_settings_ver{Model_Version}/comps_indexed.joblib')

    job_description = clean_text(job_description)

    # Vectorize user's skills and job descriptions
    job_desc = pd.DataFrame(vec_desc.transform([job_description]).todense())
    job_desc.columns = vec_desc.get_feature_names_out()
    job_skls = pd.DataFrame(vec_skills.transform([job_skills]).todense())
    job_skls.columns = vec_skills.get_feature_names_out()
    user_t = pd.DataFrame(vec_title.transform([job_title]).todense())
    user_t.columns = vec_title.get_feature_names_out()
    mat = pd.concat([user_t, job_skls, job_desc], axis=1)
    
    job_comps = pd.DataFrame(mat)

    # --------- First Logistics Regression: Predict cluster for user ---------
    predicted_cluster = cluster_lr.predict(job_comps)[0]
    print(f"Jobs CLUSTER NUMBER: {predicted_cluster}")

    # --------- Cosine Similarity: Find distance of each job to user ---------
    cos_sim = pd.DataFrame(cosine_similarity(job_comps, comps_indexed[comps_indexed.index == predicted_cluster]))

    df['cluster_no'] = pd.to_numeric(df['cluster_no'], errors='coerce')
    samp_for_cluster = df[df['cluster_no'] == predicted_cluster]
    cos_sim = cos_sim.T.set_index(samp_for_cluster['user_id'])
    cos_sim.columns = ['score']
    top_cos_sim = cos_sim.sort_values('score', ascending=False)[:30]
    print(top_cos_sim)
    
    # --------- Second Logistics Regression: Predicted probability of user liking Job ---------
    top_jobs_features = comps.loc[top_cos_sim.index] 

    probabilities = feedback_lr.predict_proba(top_jobs_features)[:,1]  # Assuming 1 is the label for 'like'
    
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

    alpha = 0.8
    beta = 0.2

    top_cos_sim['confidence_rating'] = alpha * top_cos_sim['normalized_score'] + beta * top_cos_sim['normalized_like_probability']
    top_cos_sim = top_cos_sim.sort_values('confidence_rating', ascending=False)
   
    new_suggestions_list = []
    for user_id, data  in top_cos_sim.iterrows():
        resume_title = samp_for_cluster[samp_for_cluster['user_id'] == user_id]['title'].values[0]
        confidence_rating = round(data['confidence_rating'] * 100, 2)
        new_suggestions_list.append({
            "user_id": user_id,
            "job_id": job_id,
            "suggestions": resume_title,
            "score": confidence_rating,
            "feedback": 0  # Initial feedback value
        })
    update_feedback_database(job_id, new_suggestions_list)
    update_model_version_database(job_id, Model_Version)
    return new_suggestions_list

# ------------- initial rec -------------
# placeholder
# sel_job_id = 1
# user_skills = "HTML, CSS, react, python"
# user_title = "Frontend Delevoper"
# user_description = "made web apps using react and css"
# print(f"Resume input: {user_skills}, {user_title}, {user_description}")

# cos_sim_result = give_suggestions(sel_job_id, user_skills, user_description, user_title)
# print(f"--- Reccomendations: {cos_sim_result} ---")

# ------------- getting top rec -------------
# job_id = 1  
# top_entries = top_recommendations(job_id)
# print(top_entries)

# ------------- updating feedback -------------
# job_id=1
# user_id=18
# feedback=1
# update_user_feedback(user_id, job_id, feedback)
