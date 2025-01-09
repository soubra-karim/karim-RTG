import sys, os, django
from pathlib import Path

from sklearn.calibration import LabelEncoder
sys.path.append(Path(__file__).resolve().parent.parent.__str__())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()
from UserAuth.models import Resume,ResumetoClusters,ModelVersionResume,JobPosting,FeedbackforResume

import pandas as pd
import numpy as np
import re
import nltk
import warnings; warnings.simplefilter('ignore')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import text

from joblib import dump
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report

nltk.download('stopwords')

MODEL_VERSION = 2

def create_model():
    user_resumes = Resume.objects.prefetch_related('work_experiences', 'educations', 'resume_skills')

    resume_dict = {}
    for resume in user_resumes:
        if resume.user_id not in resume_dict:
            feedback_entry = FeedbackforResume.objects.filter(user_id=resume.user_id).first()
            if feedback_entry:
                feedback_value = feedback_entry.feedback
            else:
                feedback_value = 0
            resume_dict[resume.user_id] = {
                'user_id': resume.user_id if resume.user else None,
                'title': [],
                'job_description': '', 
                'skills': list(resume.resume_skills.values_list('skill_name', flat=True)),
                'feedback': feedback_value
            }

        # Update the job titles and job description for the user
        for exp in resume.work_experiences.all():
            if exp.job_title not in resume_dict[resume.user_id]['title']:
                resume_dict[resume.user_id]['title'].append(exp.job_title)
            # Assuming the job descriptions are the same, update if it's not set yet
            if not resume_dict[resume.user_id]['job_description']:
                resume_dict[resume.user_id]['job_description'] = exp.job_description

    resume_list = list(resume_dict.values())
    return resume_list

def text_scrubber(values):
    result = []
    for item in values:
        # Ensure the function can handle both individual strings and collections of strings.
        if isinstance(item, str):
            items_to_process = [item]  # Wrap the string in a list for uniform processing.
        elif isinstance(item, list) or isinstance(item, np.ndarray):
            items_to_process = item
        else:
            continue  # Skip items that are neither strings nor lists/arrays of strings.

        # Process each item in items_to_process.
        for text in items_to_process:
            cleaned_text = text.replace("-", " ").replace("\n", " ").lower()  # Remove dashes and new lines, convert to lowercase.
            result.append(cleaned_text)
    return result

def clean_text(text):
    # Replace newline characters with space
    cleaned_text = text.replace("&nbsp;", " ").replace("\x92", " ").replace("\x95", " ").replace('&amp;', " ") \
        .replace('*', " ").replace(".", "").replace("co&#39;s", "").replace("\xae&quot;", "") \
        .replace("&#39;s", "").replace("&quot;", "").replace("?", "").replace("&#39;s", "") \
        .replace("@", "").replace("\x96", "").replace("(", "").replace(")", "") \
        .replace("+", "").replace("—", "").replace(":", "").replace(",", "").replace("/", " ") \
        .replace("\n", " ").replace("\r\n", " ")
    cleaned_text = cleaned_text.lower()
    # Remove numbers
    cleaned_text = re.sub(r'\d+', '', cleaned_text)
    # Remove punctuation
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
    return cleaned_text

def populate_resume_clusters():
    for index, row in df.iterrows():
        user_id = index
        cluster_no = row['cluster_no']
        resume, created = ResumetoClusters.objects.get_or_create(user_id=user_id,cluster=cluster_no)

    return resume

def update_model_version_database(MODEL_VERSION):
    # Convert the MODEL_VERSION number to a string, as the model fields are CharFields
    model_version_str = str(MODEL_VERSION)

    # Get all user instances from the User table
    jobs = JobPosting.objects.all()
    # Now create or update ModelVersion entries for each user
    for job in jobs:
        ModelVersionResume.objects.update_or_create(
            job_posting_id=job.id,
            defaults={
                'latest_version': model_version_str  # Update the latest model version
            }
        )

def train_model():
    # -------------- Start Script --------------
    print("---- Starting to train model ----")

    df['title'] = df['title'].apply(lambda x: text_scrubber([x])[0])
    df['skills'] = df['skills'].apply(lambda x: text_scrubber([x])[0])

    df['desc'] = df['job_description'].apply(clean_text)
    df.drop('job_description', axis=1, inplace=True)

    mine = ['manager', 'amp', 'nbsp', 'responsibilities', 'used', 'skills',
             'duties', 'work', 'worked', 'daily','services', 'job', 'using',
            'com', 'end', 'prepare', 'prepared', 'lead', 'requirements',
            'summary','Job Role','Position', "applicant", "application",
            "available", "candidate", "career", "commitment", "company",
            "competitive", "comprehensive", "consideration", "deadline",
            "degree", "description", "duties", "education", "employer",
            "employment", "encourage", "equal", "experience", "expertise",
            "field", "fill", "following", "hire", "hiring", "include",
            "including", "individual", "industry", "information", "job",
            "knowledge", "learn", "looking", "management", "manager",
            "opportunity", "position", "professional", "qualifications",
            "qualified", "responsibilities", "resume", "role", "salary",
            "seek", "seeking", "skills", "strong", "submit", "success",
            "successful", "support", "team", "title", "work", "working",
            "years", "responsibility", "required", "requirement", "requirements",
            "benefit", "benefits", "company", "companies", "task", "tasks",
            "environment", "growth", "goal", "goals", "objective", "objectives",
            "mission", "vision", "value", "values", "culture", "employee",
            "employees", "staff", "client", "clients", "customer", "customers",
            'see job description', 'n/a', 'not applicable', 'none', 'no skills required', 
            'please see job description', 'refer to job description','you','your',
            'young','yrs',"apply", "appoint", "appointment",]

    vectorizer_title = TfidfVectorizer(max_features=500, ngram_range=(1, 5))
    vectorizer_description = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), token_pattern='[a-zA-z]{3,50}', max_df=0.2, min_df=5, max_features=10000, stop_words=list(text.ENGLISH_STOP_WORDS.union(list(mine))), decode_error='ignore', vocabulary=None, binary=False) #(max_features=1000, ngram_range=(1, 3))
    vectorizer_skills = TfidfVectorizer(max_features=500, ngram_range=(1, 3))

    df['desc_new']=df['desc']
    description_matrix = vectorizer_description.fit_transform(df['desc_new'].values.astype('U'))
    description_matrix = pd.DataFrame(description_matrix.todense())
    description_matrix.columns = vectorizer_description.get_feature_names_out()

    df['skills_new']=df['skills']
    skills_matrix = vectorizer_skills.fit_transform(df['skills_new'].values.astype('U'))
    skills_matrix = pd.DataFrame(skills_matrix.todense())
    skills_matrix.columns = vectorizer_skills.get_feature_names_out()

    df['title_new']=df['title']
    title_matrix = vectorizer_title.fit_transform(df['title_new'].values.astype('U'))
    title_matrix = pd.DataFrame(title_matrix.todense())
    title_matrix.columns = vectorizer_title.get_feature_names_out()

    jobtitle_matrix = pd.concat([title_matrix, skills_matrix, description_matrix], axis=1)
    jobtitle_matrix.index = df.index
    print(jobtitle_matrix)
    comps = pd.DataFrame(jobtitle_matrix)
    print("Number of features:", comps.shape[1])

    # -------------- K Means --------------
    kmeans = KMeans(n_clusters=7)
    df['cluster_no'] = kmeans.fit_predict(comps)

    # -------------- LogisticRegression Cluster -------------
    X = comps
    y = df['cluster_no']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    cluster_lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
    cluster_lr.fit(X_train, y_train)
    y_pred = cluster_lr.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

   # -------------- LogisticRegression Feedback --------------
    X = comps  
    y_feedback = df['feedback'].replace([np.inf, -np.inf], np.nan)  # Replace Inf with NaN
    y_feedback = y_feedback.dropna()  
    y_feedback = y_feedback.astype(int)
    if y_feedback.dtype == object or not np.issubdtype(y_feedback.dtype, np.integer):
        le = LabelEncoder()
        y_feedback = le.fit_transform(y_feedback)

    X_train, X_test, y_train, y_test = train_test_split(X, y_feedback, test_size=0.2, random_state=42)
    feedback_lr = LogisticRegression(max_iter=1000, random_state=42) #LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)

    feedback_lr.fit(X_train, y_train)
    y_pred = feedback_lr.predict(X_test)

    print("Accuracy for probability:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(comps)

    # -------------- Save Model Components --------------
    dir_path = f'model_settings_ver{MODEL_VERSION}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dump(feedback_lr, os.path.join(dir_path, 'feedback_lr.joblib'))
    dump(comps, os.path.join(dir_path, 'comps.joblib'))

    comps['cluster_no'] = y.values
    comps.set_index('cluster_no', inplace=True)
    print(comps)

    # -------------- Save Model Components --------------
    dump(vectorizer_title, os.path.join(dir_path, 'vectorizer_title.joblib'))
    dump(vectorizer_skills, os.path.join(dir_path, 'vectorizer_skills.joblib'))
    dump(vectorizer_description, os.path.join(dir_path, 'vectorizer_description.joblib'))
    dump(cluster_lr, os.path.join(dir_path, 'cluster_lr.joblib'))
    dump(comps, os.path.join(dir_path, 'comps_indexed.joblib'))
    

# print(f"----- MODEL VERSION {MODEL_VERSION} -----")
# jobs = create_model()
# df = pd.DataFrame(jobs)
# df = df.set_index('user_id')
# print(df)
# print("----- Training Model -----")
# train_model()
# print("----- Deleting all Resume to Cluster Table -----")
# ResumetoClusters.objects.all().delete()
# print("----- Updating Resume to Cluster Table -----")
# populate_resume_clusters()
# print("----- Updating Model Version Resume Table -----")
# update_model_version_database(MODEL_VERSION)
