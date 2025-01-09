import sys, os, django
from pathlib import Path

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
sys.path.append(Path(__file__).resolve().parent.parent.__str__())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()
from UserAuth.models import Resume,ResumetoClusters,ModelVersionResume,JobPosting

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

rcParams['figure.figsize'] = 50, 20
start=time.time()
nltk.download('stopwords')

# Functions to clean skills data and make a vocabulary for skills vectorization
common_placeholders = [
    'see job description', 'n/a', 'not applicable', 'none', 'no skills required', 
    'please see job description', 'refer to job description'
]

def create_model():
    # Fetch the resumes and prefetch related work experiences, educations, projects, and skills
    user_resumes = Resume.objects.prefetch_related('work_experiences', 'educations', 'projects', 'resume_skills')

    # Initialize a dictionary to store resume information with user_id as the key
    resume_dict = {}

    for resume in user_resumes:
        # Check if the user already has an entry in the resume_dict
        if resume.user_id not in resume_dict:
            # Create an entry if it does not exist
            resume_dict[resume.user_id] = {
                # 'resume_id': resume.id,
                'user_id': resume.user_id if resume.user else None,
                'title': [],
                'job_description': '',  # Assuming all descriptions are the same; will be updated later
                'skills': list(resume.resume_skills.values_list('skill_name', flat=True))
            }

        # Update the job titles and job description for the user
        for exp in resume.work_experiences.all():
            if exp.job_title not in resume_dict[resume.user_id]['title']:
                resume_dict[resume.user_id]['title'].append(exp.job_title)
            # Assuming the job descriptions are the same, update if it's not set yet
            if not resume_dict[resume.user_id]['job_description']:
                resume_dict[resume.user_id]['job_description'] = exp.job_description

    # Convert the resume_dict to a list format
    resume_list = list(resume_dict.values())

    return resume_list

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
    all_skills = [] 
    for index, row in df.iterrows():
        skills = row['skills']  # Get the skills string
        if pd.notnull(skills):  # Check if the skills string is not NaN
            skills_list = skills.split(',')  # Split the string into individual skills
            cleaned_skills = [skill.strip() for skill in skills_list if skill.strip()]  # Clean and filter empty strings
            all_skills.extend(cleaned_skills)  # Add to the collective list
    
    # Create a set of unique skills, then convert it back to a list
    vocabulary = list(set(all_skills))
    
    return vocabulary

# function to clean the text in each job description
def clean_text(text):
    cleaned_text = text.replace("&nbsp;", " ").replace("\x92", " ").replace("\x95", " ").replace('&amp;', " ") \
        .replace('*', " ").replace(".", "").replace("co&#39;s", "").replace("\xae&quot;", "") \
        .replace("&#39;s", "").replace("&quot;", "").replace("?", "").replace("&#39;s", "") \
        .replace("@", "").replace("\x96", "").replace("(", "").replace(")", "") \
        .replace("+", "").replace("—", "").replace(":", "").replace(",", "").replace("/", " ")
    return cleaned_text

def train_model():
    # -------------- Start Script --------------
    print("---- Starting to train model ----")
    # Fetch job data from the database
    df['title'] = text_scrubber(df['title'])
    
    df['skills'] = text_scrubber(df['skills'])
    voc = vocab(df)

    # Apply the clean_text function to each element in the 'jobdescription' column
    df['desc'] = df['job_description'].apply(clean_text)
    df.drop('job_description', axis=1, inplace=True)

    #min_df ignores terms that are in more than 20% of documents
    mine = ['manager', 'amp', 'nbsp', 'responsibilities', 'used', 'skills', 'duties', 'work', 'worked', 'daily','services', 'job', 'using', 'com', 'end', 'prepare', 'prepared', 'lead', 'requirements','summary','Job Role','Position']

    vectorizer_title = TfidfVectorizer(max_features=500, ngram_range=(1, 5))
    vectorizer_description = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), token_pattern='[a-zA-z]{3,50}', max_df=0.2, min_df=5, max_features=10000, stop_words=list(text.ENGLISH_STOP_WORDS.union(list(mine))), decode_error='ignore', vocabulary=None, binary=False) #(max_features=1000, ngram_range=(1, 3))
    vectorizer_skills = TfidfVectorizer(vocabulary=voc, decode_error='ignore') #((max_features=500, ngram_range=(1, 1))

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

    jobtitle_matrix = pd.concat([title_matrix, skills_matrix], axis=1)#, description_matrix
    jobtitle_matrix
    comps = pd.DataFrame(jobtitle_matrix)
    print("Number of features:", comps.shape[1])

    # -------------- K Means --------------
    # from sklearn.cluster import KMeans
    # kmeans = KMeans(n_clusters=7)
    # df['cluster_no'] = kmeans.fit_predict(comps)

    # # -------------- LogisticRegression --------------
    # from sklearn.metrics import accuracy_score, classification_report
    # pca = PCA(n_components=2,random_state=42)  # Reduce to 2 dimensions for plotting
    # reduced_features = pca.fit_transform(comps)
    # reduced_features = pd.DataFrame(reduced_features)

    # X = comps
    # y = df['cluster_no']
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # # lr = LogisticRegression(max_iter=1000, random_state=42)
    # lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
    # lr.fit(X_train, y_train)
    # y_pred = lr.predict(X_test)
    # print("Accuracy:", accuracy_score(y_test, y_pred))
    # print(classification_report(y_test, y_pred))

    # # Assign cluster number to each job title in comps to pull particular cluster out for comparison
    # comps['cluster_no'] = y.values
    # comps.set_index('cluster_no', inplace=True)
    
    # ----------------------- Clusters vs Inertia -----------------------
    # clusters_range = range(1, 30)
    # inertias = []
    # X = comps

    # for n_clusters in clusters_range:
    #     kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    #     kmeans.fit(X)
    #     inertias.append(kmeans.inertia_)
    
    # plt.figure(figsize=(10, 6))
    # plt.plot(clusters_range, inertias, '-o')
    # plt.title('Elbow Method For Optimal Number of Clusters')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('Inertia')
    # plt.xticks(clusters_range)
    # plt.show()

    # ----------------------- Clusters vs Silhouette Score -----------------------
    from sklearn.metrics import silhouette_score
    # Assuming 'comps' is your features matrix
    X = comps
    # Range of clusters to try
    clusters_range = range(2, 15)
    silhouette_scores = []
    for n_clusters in clusters_range:
        print(n_clusters)
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

    # ----------------------- Silhouette Diagrams -----------------------
    # from sklearn.metrics import silhouette_samples, silhouette_score
    # import matplotlib.cm as cm
    # import matplotlib.pyplot as plt
    # from sklearn.cluster import KMeans

    # # Assuming 'X' is your data matrix
    # range_n_clusters = [5,10,15,20,25,30]  # Specify the range of clusters you want to evaluate
    # X = comps

    # for n_clusters in range_n_clusters:
    #     # Create a subplot with 1 row and 1 column
    #     fig, ax1 = plt.subplots(1, 1)
    #     fig.set_size_inches(18, 7)

    #     # The 1st subplot is the silhouette plot
    #     # The silhouette coefficient can range from -1, 1 but in this example all
    #     # lie within [-0.1, 1]
    #     ax1.set_xlim([-0.1, 1])
    #     # The (n_clusters+1)*10 is for inserting blank space between silhouette
    #     # plots of individual clusters, to demarcate them clearly.
    #     ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    #     # Initialize the clusterer with n_clusters value and a random generator
    #     # seed of 10 for reproducibility.
    #     clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    #     cluster_labels = clusterer.fit_predict(X)

    #     # The silhouette_score gives the average value for all the samples.
    #     # This gives a perspective into the density and separation of the formed
    #     # clusters
    #     silhouette_avg = silhouette_score(X, cluster_labels)
    #     print(f"For n_clusters = {n_clusters}, the average silhouette_score is : {silhouette_avg}")

    #     # Compute the silhouette scores for each sample
    #     sample_silhouette_values = silhouette_samples(X, cluster_labels)

    #     y_lower = 10
    #     for i in range(n_clusters):
    #         # Aggregate the silhouette scores for samples belonging to
    #         # cluster i, and sort them
    #         ith_cluster_silhouette_values = \
    #             sample_silhouette_values[cluster_labels == i]

    #         ith_cluster_silhouette_values.sort()

    #         size_cluster_i = ith_cluster_silhouette_values.shape[0]
    #         y_upper = y_lower + size_cluster_i

    #         color = cm.nipy_spectral(float(i) / n_clusters)
    #         ax1.fill_betweenx(np.arange(y_lower, y_upper),
    #                         0, ith_cluster_silhouette_values,
    #                         facecolor=color, edgecolor=color, alpha=0.7)

    #         # Label the silhouette plots with their cluster numbers at the middle
    #         ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

    #         # Compute the new y_lower for next plot
    #         y_lower = y_upper + 10  # 10 for the 0 samples

    #     ax1.set_title("The silhouette plot for the various clusters.")
    #     ax1.set_xlabel("The silhouette coefficient values")
    #     ax1.set_ylabel("Cluster label")

    #     # The vertical line for average silhouette score of all the values
    #     ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    #     ax1.set_yticks([])  # Clear the yaxis labels / ticks
    #     ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    #     # Labeling the silhouette plots with their cluster numbers
    #     plt.suptitle(f"Silhouette analysis for KMeans clustering on sample data with n_clusters = {n_clusters}",
    #                 fontsize=14, fontweight='bold')

    # plt.show()

    # ----------------------- Plot applicants PCA -----------------------
    # from sklearn.decomposition import PCA
    # import matplotlib.pyplot as plt
    # # Assuming 'comps' is the matrix containing your job postings data after TF-IDF and other preprocessing
    # # Let's first reduce the data to 2 dimensions using PCA
    # pca = PCA(n_components=2)
    # reduced_data = pca.fit_transform(jobtitle_matrix)
    # # Now we can plot the first 2 components of each data point
    # plt.figure(figsize=(10, 10))
    # plt.scatter(reduced_data[:, 0], reduced_data[:, 1], alpha=0.5)
    # plt.title('Job Postings Plot')
    # plt.xlabel('PCA Component 1')
    # plt.ylabel('PCA Component 2')
    # plt.show()

    # ----------------------- Plot applicants TSNE -----------------------
    # from sklearn.manifold import TSNE
    # # Use t-SNE to reduce dimensions, this might take a while if 'comps' is large
    # tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    # tsne_results = tsne.fit_transform(comps)
    # plt.figure(figsize=(10, 10))
    # plt.scatter(tsne_results[:, 0], tsne_results[:, 1], alpha=0.5)
    # plt.title('Job Postings Plot with t-SNE')
    # plt.xlabel('t-SNE Feature 1')
    # plt.ylabel('t-SNE Feature 2')
    # plt.show()

    # ----------------------- Plot applicants UMAP -----------------------
    # import umap
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D

    # # Assuming 'comps' is your high-dimensional data
    # reducer = umap.UMAP(n_components=3, n_neighbors=30, min_dist=0.0, metric='euclidean', random_state=42)
    # embedding = reducer.fit_transform(comps)

    # # Plot the embedding in 3D
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(embedding[:, 0], embedding[:, 1], embedding[:, 2], s=5)
    # plt.title('3D UMAP')
    # ax.set_xlabel('UMAP Dimension 1')
    # ax.set_ylabel('UMAP Dimension 2')
    # ax.set_zlabel('UMAP Dimension 3')
    # plt.show()

    # ------------------ 3D Visualization ------------------
    # from sklearn.decomposition import PCA

    # pca = PCA(n_components=3, random_state=42)  # Use 3 components for 3D visualization
    # reduced_features_3d = pca.fit_transform(comps)
    # reduced_features_3d = pd.DataFrame(reduced_features_3d, columns=['PC1', 'PC2', 'PC3'])
    # reduced_features_3d['cluster_no'] = df['cluster_no']
    
    # from mpl_toolkits.mplot3d import Axes3D
    # import matplotlib.pyplot as plt
    # import seaborn as sns

    # # Plotting
    # fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111, projection='3d')

    # # Scatter plot
    # scatter = ax.scatter(reduced_features_3d['PC1'], reduced_features_3d['PC2'], reduced_features_3d['PC3'], 
    #                     c=reduced_features_3d['cluster_no'], cmap='viridis', s=50, alpha=0.6)

    # # Title and labels
    # ax.set_title('3D Cluster Visualization')
    # ax.set_xlabel('PC1')
    # ax.set_ylabel('PC2')
    # ax.set_zlabel('PC3')

    # # Legend
    # legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    # ax.add_artist(legend1)

    # plt.show()

# print(f"----- MODEL VERSION TESTING -----")
# jobs = create_model()
# df = pd.DataFrame(jobs)
# print("----- Training Model -----")
# train_model()
# print("----- Deleting all Resume to Cluster Table -----")
# ResumetoClusters.objects.all().delete()
# print("----- Updating Resume to Cluster Table -----")
# populate_resume_clusters()
# print("----- Updating Model Version Resume Table -----")
# update_model_version_database(MODEL_VERSION)