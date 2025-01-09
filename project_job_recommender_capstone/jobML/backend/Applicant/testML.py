import sys, os, django
from matplotlib import pyplot as plt
from matplotlib.mlab import GaussianKDE
from sklearn.preprocessing import normalize
from pathlib import Path
sys.path.append(Path(__file__).resolve().parent.parent.__str__())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()
from UserAuth.models import JobPosting,JobToClusters

import pandas as pd
import numpy as np
import re
import time
import nltk
import warnings; warnings.simplefilter('ignore')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import text
from pylab import rcParams
from nltk.corpus import stopwords
from joblib import dump
from django.conf import settings
from views import create_model

rcParams['figure.figsize'] = 50, 20
start=time.time()
nltk.download('stopwords')

# Functions to clean skills data and make a vocabulary for skills vectorization
common_placeholders = [
    'see job description', 'n/a', 'not applicable', 'none', 'no skills required', 
    'please see job description', 'refer to job description'
]

def text_scrubber(values):
    result = []
    for item in values:
        # If 'item' is a list or an array, handle it appropriately
        if isinstance(item, list) or isinstance(item, np.ndarray):
            item = ', '.join([str(i) for i in item])  # Convert list/array to string
            temp = item.lower()  # Convert to lowercase
            temp = re.sub(r'\(.*\)|&#39;|\x92', '', temp)  # Remove unwanted characters
            temp = re.sub(r' &amp; |&amp;|\x95|:|;|&|\.|/| and ', ',', temp)  # Replace certain characters with comma
            temp = [skill.strip() for skill in temp.split(',') if skill.strip()] # split the skills into a list and remove empty entries
            temp = ','.join(temp) # Rejoin the cleaned skills into a string separated by commas
            result.append(temp)
    return result

def vocab(df):
    all_skills = []  # List to collect all skills
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        skills = row['skills']  # Get the skills string
        if pd.notnull(skills):  # Check if the skills string is not NaN
            skills_list = skills.split(',')  # Split the string into individual skills
            cleaned_skills = [skill.strip() for skill in skills_list if skill.strip()]  # Clean and filter empty strings
            all_skills.extend(cleaned_skills)  # Add to the collective list
    
    # Create a set of unique skills, then convert it back to a list
    vocabulary = list(set(all_skills))
    
    return vocabulary

# Define a function to clean the text in each job description
def clean_text(text):
    cleaned_text = text.replace("&nbsp;", " ").replace("\x92", " ").replace("\x95", " ").replace('&amp;', " ") \
        .replace('*', " ").replace(".", "").replace("co&#39;s", "").replace("\xae&quot;", "") \
        .replace("&#39;s", "").replace("&quot;", "").replace("?", "").replace("&#39;s", "") \
        .replace("@", "").replace("\x96", "").replace("(", "").replace(")", "") \
        .replace("+", "").replace("—", "").replace(":", "").replace(",", "").replace("/", " ")
    return cleaned_text

# Fetch job data from the database
print("---- Starting to train model ----")
jobs = create_model()
df = pd.DataFrame(jobs)

df['skills'] = text_scrubber(df['skills'])
c

# Apply the clean_text function to each element in the 'jobdescription' column
df['desc'] = df['job_description'].apply(clean_text)
df.drop('job_description', axis=1, inplace=True)

mine = ['manager', 'amp', 'nbsp', 'responsibilities', 'used', 'skills', 'duties', 'work', 'worked', 'daily','services', 'job', 'using', 'com', 'end', 'prepare', 'prepared', 'lead', 'requirements','summary','Job Role','Position']

vectorizer_title = TfidfVectorizer(max_features=500, ngram_range=(1, 5))
vectorizer_description = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), token_pattern='[a-zA-z]{3,50}', max_df=0.2, min_df=5, max_features=10000, stop_words=list(text.ENGLISH_STOP_WORDS.union(list(mine))), decode_error='ignore', vocabulary=None, binary=False) #(max_features=1000, ngram_range=(1, 3))
vectorizer_skills = TfidfVectorizer(vocabulary=voc, decode_error='ignore') #((max_features=500, ngram_range=(1, 1))

title_matrix = vectorizer_title.fit_transform(df['title'].values.astype('U'))
description_matrix = vectorizer_description.fit_transform(df['desc'].values.astype('U'))
skills_matrix = vectorizer_skills.fit_transform(df['skills'].values.astype('U'))

title_matrix.columns = vectorizer_title.get_feature_names_out()
description_matrix.columns = vectorizer_description.get_feature_names_out()
skills_matrix.columns = vectorizer_skills.get_feature_names_out()

title_matrix = pd.DataFrame(title_matrix.todense())
description_matrix = pd.DataFrame(description_matrix.todense())
skills_matrix = pd.DataFrame(skills_matrix.todense())

combined_matrix = pd.concat([title_matrix, description_matrix, skills_matrix], axis=1)
# print(combined_matrix)

# Normalize the combined matrix to ensure equal weighting before clustering
# combined_matrix_normalized = normalize(combined_matrix, axis=0)

# -------------- K Means --------------
from sklearn.cluster import KMeans

pca = PCA(n_components=574,random_state=42)  # Reduce to 2 dimensions for plotting
reduced_features = pca.fit_transform(combined_matrix)
reduced_features = pd.DataFrame(reduced_features)

n_clusters = 6
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(combined_matrix)

unique_clusters = np.unique(df['cluster'])
colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_clusters)))
# cluster_centers_2D = pca.transform(kmeans.cluster_centers_)

# for cluster, color in zip(unique_clusters, colors):
#     cluster_subset = reduced_features[df['cluster'] == cluster]
#     job_ids = df[df['cluster'] == cluster]['id'].values 

#     plt.scatter(cluster_subset[:, 0], cluster_subset[:, 1], s=20, c=[color], label=f'Cluster {cluster}')

#     for i, job_id in enumerate(job_ids):
#         plt.annotate(job_id, (cluster_subset[i, 0], cluster_subset[i, 1]), fontsize=8, alpha=0.7)


# # Plot the cluster centers
# plt.scatter(cluster_centers_2D[:, 0], cluster_centers_2D[:, 1], s=100, c='black', marker='x', linewidths=2, label='Centers')
# plt.title('Jobs Clustering with KMeans, Centers Marked')
# plt.xlabel('Reduced Component 1')
# plt.ylabel('Reduced Component 2')
# plt.legend()
# plt.show()

# -------------- DBSCAN --------------

# from sklearn.cluster import DBSCAN
# # Assuming X is your feature matrix
# dbscan = DBSCAN(eps=0.4, min_samples=2)
# df['cluster'] = dbscan.fit_predict(reduced_features)
# unique_labels = set(df['cluster'])
# # Colors for each cluster (and possibly noise)
# colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise
#         col = [0, 0, 0, 1]

#     class_member_mask = (df['cluster'] == k)
#     xy = reduced_features[class_member_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

# plt.title('DBSCAN Clustering')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.show()

# for k in unique_labels:
#     if k != -1:  # Exclude noise
#         cluster_points = reduced_features[df['cluster'] == k]
#         center = cluster_points.mean(axis=0)
#         plt.plot(center[0], center[1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', marker='x', markersize=10)

# plt.title('DBSCAN Clustering with Approximated Centers')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.show()

# ----------- Accuracy ---------------------
from sklearn.metrics import accuracy_score, classification_report

X = reduced_features
y = df['cluster']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

feature_names = df.columns
coefficients = log_reg.coef_

for i, cluster_coefficients in enumerate(coefficients):
    print(f"Cluster {i}:")
    for feature_name, coef in zip(feature_names, cluster_coefficients):
        print(f"{feature_name}: {coef}")
    print("\n")

# print(df)
print(reduced_features)

# Save your model components
dump(vectorizer_title, 'saved_model2/vectorizer_title.joblib')
dump(vectorizer_description, 'saved_model2/vectorizer_description.joblib')
dump(vectorizer_skills, 'saved_model2/vectorizer_description.joblib')
dump(pca, 'saved_model2/pca.joblib')
dump(log_reg, 'saved_model2/lr.joblib')
dump(reduced_features, 'saved_model2/comps.joblib')

def populate_job_clusters():
    for index, row in df.iterrows():
        job_id = row['id']
        cluster_no = row['cluster']
        job, created = JobToClusters.objects.get_or_create(job_posting_id=job_id,cluster=cluster_no)

    return job

JobToClusters.objects.all().delete()
populate_job_clusters()

print("Done Training")
# df.to_json('model_settings/df.json')