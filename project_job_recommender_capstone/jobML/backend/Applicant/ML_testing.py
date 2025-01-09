import sys, os, django
from pathlib import Path

from sklearn.calibration import LabelEncoder
sys.path.append(Path(__file__).resolve().parent.parent.__str__())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()
from UserAuth.models import JobPosting,JobToClusters,ModelVersion,User,FeedbackforJob

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
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report


def create_model():
    # Fetch the job postings and prefetch the related skills
    jobpostings = JobPosting.objects.prefetch_related('skills')

    # Transform the job postings into the desired structure
    jobpostings_list = []
    for jp in jobpostings:
        skills = list(jp.skills.values_list('skill_name', flat=True))
        jobpostings_list.append({
            'id': jp.id,
            'title': jp.title,
            'job_description': jp.job_description,
            'skills': skills,
        })

    return jobpostings_list

def text_scrubber(values):
    result = []
    for item in values:
        if isinstance(item, list) or isinstance(item, np.ndarray):
            # Join skills into a single string separated by spaces instead of commas
            temp = ' '.join(item)
            result.append(temp.lower())  # Keep it lowercase for consistency
    return result

def inertiaCluster(comps):
    clusters_range = range(2, 30)
    inertias = []
    X = comps

    for n_clusters in clusters_range:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(clusters_range, inertias, '-o')
    plt.title('Elbow Method For Optimal Number of Clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.xticks(clusters_range)
    plt.show()

def silCluster(comps):
    from sklearn.metrics import silhouette_score
    X = comps
    clusters_range = range(2, 30)
    silhouette_scores = []
    for n_clusters in clusters_range:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X)
        score = silhouette_score(X, kmeans.labels_)
        silhouette_scores.append(score)
    # Plot silhouette scores
    plt.figure(figsize=(10, 6))
    plt.plot(clusters_range, silhouette_scores, '-o')
    plt.title('Silhouette Score For Optimal Number of Clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')
    plt.xticks(clusters_range)
    plt.show()

def plotPCA(comps):
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    # Assuming 'comps' is the matrix containing your job postings data after TF-IDF and other preprocessing
    # Let's first reduce the data to 2 dimensions using PCA
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(comps)
    # Now we can plot the first 2 components of each data point
    plt.figure(figsize=(10, 10))
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], alpha=0.5)
    plt.title('Job Postings Plot')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()

def plotTSNE(comps):
    from sklearn.manifold import TSNE
    # Use t-SNE to reduce dimensions, this might take a while if 'comps' is large
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    tsne_results = tsne.fit_transform(comps)
    plt.figure(figsize=(10, 10))
    plt.scatter(tsne_results[:, 0], tsne_results[:, 1], alpha=0.5)
    plt.title('Job Postings Plot with t-SNE')
    plt.xlabel('t-SNE Feature 1')
    plt.ylabel('t-SNE Feature 2')
    plt.show()

def visualCluster(comps):
    
    # Assuming 'comps' is your data and 'df' is a DataFrame with the same data prepared for clustering
    kmeans = KMeans(n_clusters=22, random_state=42)
    df['cluster_no'] = kmeans.fit_predict(comps)

    pca = PCA(n_components=2, random_state=42)
    reduced_features = pca.fit_transform(comps)

    plt.figure(figsize=(10, 10))
    scatter = plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=df['cluster_no'], cmap='gist_ncar', s=50, alpha=0.6)
    plt.title('Clusters Visualization with PCA')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')

    # Create a colorbar with the correct number of labels.
    # Generate the labels based on the number of unique clusters.
    num_clusters = len(df['cluster_no'].unique())
    colorbar = plt.colorbar(scatter, ticks=range(num_clusters))
    colorbar.set_ticklabels(range(num_clusters))

    plt.show()

    # ------------------------------------------------------------
    # kmeans = KMeans(n_clusters=22, random_state=42)
    # clusters = kmeans.fit_predict(comps)

    # # Perform PCA for dimensionality reduction for visualization
    # pca = PCA(n_components=2, random_state=42)
    # reduced_features = pca.fit_transform(comps)
    # centroids = pca.transform(kmeans.cluster_centers_)

    # # Create a scatter plot of the reduced features with the clusters color-coded
    # plt.figure(figsize=(14, 10))
    # plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=clusters, cmap='tab20', s=50, alpha=0.6)

    # # Overlay the centroids on the same plot as black 'X'
    # plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=200, marker='X')

    # # Set the title and axis labels
    # plt.title('Clusters Visualization', fontsize=20)
    # plt.xlabel('Principal Component 1', fontsize=16)
    # plt.ylabel('Principal Component 2', fontsize=16)

    # # Create a colorbar with ticks and labels
    # cbar = plt.colorbar(boundaries=np.arange(-0.5, 22, 1))
    # cbar.set_ticks(np.arange(0, 22, 1))
    # cbar.set_ticklabels([f'Cluster {i}' for i in range(22)])

    # # Show the plot
    # plt.show()

def threeDCluster(comps):
    from sklearn.decomposition import PCA

    pca = PCA(n_components=3, random_state=42)  # Use 3 components for 3D visualization
    reduced_features_3d = pca.fit_transform(comps)
    reduced_features_3d = pd.DataFrame(reduced_features_3d, columns=['PC1', 'PC2', 'PC3'])
    reduced_features_3d['cluster_no'] = df['cluster_no']
    
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Plotting
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    scatter = ax.scatter(reduced_features_3d['PC1'], reduced_features_3d['PC2'], reduced_features_3d['PC3'], 
                        c=reduced_features_3d['cluster_no'], cmap='viridis', s=50, alpha=0.6)

    # Title and labels
    ax.set_title('3D Cluster Visualization')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    # Legend
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)
    plt.show()

def create_model_with_feedback():
    # Fetch job postings and user feedback
    job_postings = JobPosting.objects.prefetch_related('skills')
    feedbacks = FeedbackforJob.objects.all()
    
    # Here, assume `feedbacks` is a queryset of feedback instances, which need to be transformed into a DataFrame
    feedbacks_df = pd.DataFrame(list(feedbacks.values('job_posting_id', 'feedback')))
    
    # Transform job postings into DataFrame as before
    jobpostings_list = []
    for jp in job_postings:
        skills = list(jp.skills.values_list('skill_name', flat=True))
        jobpostings_list.append({
            'id': jp.id,
            'title': jp.title,
            'job_description': jp.job_description,
            'skills': skills,
        })
    jobs_df = pd.DataFrame(jobpostings_list)
    
    # Join job postings with feedback
    df = pd.merge(jobs_df, feedbacks_df, left_on='id', right_on='job_posting_id', how='left')
    
    # Fill missing feedback with a neutral value, e.g., 0, if you decide neutral feedback is appropriate
    df['feedback'] = df['feedback'].fillna(0)
    
    return df

def logisticReg(df, comps):
    X = comps
    y = df['cluster_no']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    cluster_lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
    
    cluster_lr.fit(X_train, y_train)
    y_pred = cluster_lr.predict(X_test)
    
    print("Accuracy for cluster:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Assign cluster number to each job title in comps to pull particular cluster out for comparison
    comps['cluster_no'] = y.values
    comps.set_index('cluster_no', inplace=True)

    return cluster_lr

def logisticRegFeedback(df, comps):
    X = comps  

    y = df['feedback'].replace([np.inf, -np.inf], np.nan)  # Replace Inf with NaN
    y = y.dropna()  
    y = y.astype(int)
    if y.dtype == object or not np.issubdtype(y.dtype, np.integer):
        le = LabelEncoder()
        y = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    feedback_lr = LogisticRegression(max_iter=1000, random_state=42) #LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)

    feedback_lr.fit(X_train, y_train)
    y_pred = feedback_lr.predict(X_test)

    print("Accuracy for probability:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    return feedback_lr

def settingsDump(MODEL_VERSION,vectorizer_title,vectorizer_skills,cluster_lr,comps,feedback_lr):
    dir_path = f'model_settings_ver{MODEL_VERSION}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dump(vectorizer_title, os.path.join(dir_path, 'vectorizer_title.joblib'))
    dump(vectorizer_skills, os.path.join(dir_path, 'vectorizer_skills.joblib'))
    dump(cluster_lr, os.path.join(dir_path, 'cluster_lr.joblib'))
    dump(feedback_lr, os.path.join(dir_path, 'feedback_lr.joblib'))
    dump(comps, os.path.join(dir_path, 'comps.joblib'))

def train_model(df):
    # -------------- Start Script --------------
    print("---- Starting to train model ----")

    # Consider reducing the ngram range and not limiting the features too much.
    vectorizer_title = TfidfVectorizer(min_df=2, max_df=0.8, ngram_range=(1, 8))

    # If the skills are simple and not phrases, a simple unigram representation might suffice.
    vectorizer_skills = TfidfVectorizer(min_df=2, max_df=0.8)

    df['skills'] = text_scrubber(df['skills'])
    df['skills_new'] = df['skills']
    skills_matrix = vectorizer_skills.fit_transform(df['skills_new'].values.astype('U'))

    df['title_new'] = df['title']
    title_matrix = vectorizer_title.fit_transform(df['title_new'].values.astype('U'))

    # Concatenate the title and skills matrices along the columns
    comps = pd.concat([pd.DataFrame(title_matrix.toarray()), pd.DataFrame(skills_matrix.toarray())], axis=1)

    # -------------- K Means --------------
    kmeans = KMeans(n_clusters=20)
    df['cluster_no'] = kmeans.fit_predict(comps)

    # # -------------- LogisticRegression --------------
    cluster_lr = logisticReg(df,comps)
    feedback_lr = logisticRegFeedback(df,comps)
    MODEL_VERSION = 0
    settingsDump(MODEL_VERSION,vectorizer_title,vectorizer_skills,cluster_lr,comps,feedback_lr)


    # ------------------- Visualizing Clusters ----------------------
    # visualCluster(comps)
    
    # ------------------- Clusters vs Inertia -----------------------
    # inertiaCluster(comps)

    # ------------------ Clusters vs Silhouette Score ---------------
    # silCluster(comps)

    # ------------------ Plot applicants PCA ------------------------
    # plotPCA(comps)

    # ------------------ Plot applicants TSNE -----------------------
    # plotTSNE(comps)

    # ------------------ 3D Visualization ---------------------------
    # threeDCluster(comps)


# print(f"----- MODEL VERSION TESTING -----")
# # jobs = create_model()
# data = create_model_with_feedback()
# df = pd.DataFrame(data)
# print("----- Training Model -----")
# train_model(df)