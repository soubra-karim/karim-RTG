from selenium import webdriver
import nltk
nltk.download('punkt')
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import ngrams
import time
from bs4 import BeautifulSoup
import pprint
import pickle
import re
import pandas as pd
import uuid
import json
from django.conf import settings
import django
import os
from ResumeScraper.resume import ResumeExtractor
from django.db.models import Q
import re

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

def run():
    print('hi')

class scrapejob:

    def __init__(self,website:str):
        """
            website(string): indeed or glassdoor
        """
        

        # application = get_wsgi_application()
        self.jobs_to_upload=[]
        self.jobs_to_check=[]
        # self.upload_jobs=UploadJob()
        opt= Options()
        opt.add_argument("--disable-popup-blocking")
        opt.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(opt)
        self.driver.implicitly_wait(3)
        self.indeed=False
        self.gdoor=False
        if website == "indeed":
            self.indeed=True
            self.link="https://ca.indeed.com/"
        elif website == "glassdoor":
            self.gdoor=True
            pass
        else:
            raise Exception("website must be indeed or glassdoor")


    #need this to connect 
    def connect(self):
        self.driver.get(self.link)
        self.driver.maximize_window()
        time.sleep(5)


    #need this for searching job and closing pop up
    def search_job(self,job_name:str):
        """
            job_name(str): jobs to look up
        """
            
        if(self.indeed):
            element = self.driver.find_element(By.ID,"text-input-what") # find search box
            element.clear()
            element.send_keys(job_name)
            element.send_keys(Keys.RETURN)
            time.sleep(3)
            self.driver.find_element("xpath","//a[@class='css-145oca5 emf9s7v0']").click() #set to find newest job posts
            time.sleep(3)
            while(True):
                try:
                    
                    e=self.driver.find_elements("xpath", "//button[@class='css-yi9ndv e8ju0x51']") # close the pop up
                    time.sleep(3)
                        
                    if(len(e)!=0):     
                        e[0].click()

                        time.sleep(3)
                        
                        break
                    else:
                        pass
                except:
                    pass
        time.sleep(3)


    def scrape_job_data(self,limit:int=100000000000):
        """
            collects job postings until limit is met.
            limit(int)= number of job posts to collect
        """
        #         job_posting_data = {
        #     "title": row['jobtitle'],
        #     "company_name": row['company'],
        #     "location": row['joblocation_address'],
        #     "job_description": row['jobdescription'],
        #     "posted_date": timezone.now(),
        #     "application_deadline": timezone.now() + timezone.timedelta(days=100),
        #     "experience_required": "N/A",
        #     "creator": None,
        # }
        extract_info = ResumeExtractor()
        job_count=0
        while(job_count<limit):
            time.sleep(3)
            jobs = self.driver.find_elements("xpath","//li[@class='css-5lfssm eu4oa1w0']")
           

            
            for job in jobs:
                
                
                try:
                    
                    job.click()
                    time.sleep(3)
                except:
                    continue
                try:
                    doc=BeautifulSoup(self.driver.page_source,"html.parser")
                    job_title = doc.find("h2",class_="jobsearch-JobInfoHeader-title css-1t78hkx e1tiznh50")
                    company_name=doc.find("span",class_="css-1cxc9zk e1wnkr790")
                    location=doc.find("div",class_="css-waniwe eu4oa1w0")
                    job_description=doc.find("div",class_="jobsearch-jobDescriptionText jobsearch-JobComponent-description css-kqe8pq eu4oa1w0")

                    job_title=job_title.get_text()
                    company_name=company_name.get_text()
            
                    location=location.get_text()
                    job_description=job_description.get_text()
                    
                    skills_found = extract_info.extract_skills(job_description).split(",")
                    pattern = r"\s*-\s*job post\b"


                    job_title = re.sub(pattern, '', job_title, flags=re.IGNORECASE)
                    job_posting_data = {
                        "title": job_title,
                        "company_name": company_name,
                        "location": location,
                        "job_description": job_description,
                        "posted_date": timezone.now(),
                        "application_deadline": timezone.now() + timezone.timedelta(days=100),
                        "experience_required": "N/A",
                        "creator": None,
                    }
                    print(job_posting_data)
                    existing_job_posting = JobPosting.objects.filter(
                        Q(title=job_posting_data["title"]) &
                        Q(company_name=job_posting_data["company_name"]) &
                        Q(location=job_posting_data["location"]) &
                        Q(job_description=job_posting_data["job_description"])
                        ).first()
                    if existing_job_posting is None:
                        job_posting = JobPosting.objects.create(**job_posting_data)
                        
                        # skills_list = current_job_data.get("skills", [])

                        for skill_name in skills_found:
                                skill, created = ListOfSkills.objects.get_or_create(skill_name=skill_name)
                                job_posting.skills.add(skill)
                        print("job uploaded!")
                        print(job_posting_data)
                        job_count+=1
                    time.sleep(3)
                    
                except:
                    pass
    def extract_skills(self,description:str):
         
           
            list_of_skills=["amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
            "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure (tables, cosmosdb, sql, etc)","microsoft azure"
            "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica","Back End","C-suite executive","Cloud Computing","Data Scientist","Data or business analyst","business analyst","data analyst","Database Administrator(DBA)","Database Administrator"
                 ,"designer","Devops","academic researcher","educator","Embedded applications","embedded devices developer","Engineering manager","Enterprise application","Front End"
                 ,"Full stack","Game developer","Information Security","Mobile Developer","Network Engineer","product manager","QA","Test developer","Sales professional","software developer","java developer"
                 ,"sudent","system administrator","web developer",".net core","agile","angular","asp.net mvc","aura","aurelia","bottle","cakephp","cassandra","catalyst","cloudera","codeigniter","cordova","couchdb","cuba",
                                "django","dojo","dropwizard","durandal","elm","ember.js","express","flask","flatiron","flex","flink","google web toolkit","grails","hadoop","halcyon","hive","hpcc",
                                "jsf","koa","laravel","lift","lithium","map reduce","mason","meteor","moustache","ninja","nitro","node.js","pentaho","phoenix","play","polymer","pyramid",
                                "rapidminer","react","revel","riot.js","ruby on rails","rum","simplex","sinatra","solar","spark","spring","storm","struts","symfony","tapestry","tensorflow","pytorch"
                                ,"tornado","vaadin","vanilla","vert.x","vue.js","web2py","wicket","xamarin","yarn","yii","zend","zope",".net","abap","abc","actionscript","ada","ajax","apex","apl","applescript","arc","arduino","asp","assembly","atlas","automator","avenue","awk","bash","bc","bourne shell","bro"
                            ,"c","c shell","c#","c++","caml","ceylon","cfml","ch","clarion","clean","clojure","cobol","cobra","coffeescript","coldfusion","css","ct","d","dart"
                            ,"dcl","pascal","e","ecl","ec","ecmascript","egl","elixir","erlang","f#","falcon","felix","forth","fortran","fortress","go","gosu","groovy","hack","haskell",
                            "html","icon","idl","inform","informix-4gl","io","java","jade","javascript","jscript","julia","korn shell","kotlin","labview","ladder logic","lingo","lisp"
                            ,"logo","lotusscript","lpc","lua","lustre","magic","mantis","mathematica","matlab","mercury","ml","monkry","moo","mumps",
                            "objective-c","ocaml","occam","ooc","opa","opencl","perl","php","pilot","sql","postscript","powerscript","powershell","puppet","python","q","r","rexx","ruby","ruby on rails"
                            ,"rust","s","s-plus","sas","scala","scilab","sed","self","shell","signal","simula","simulink","smalltalk","smarty","spark","spss","sqr","swift","tacl","tcl","tom","transact-sql"
                            ,"typescript","vb.net","vba","vbscript","verilog","vhdl","visual basic 6","xen","xquery","xslt","amazon echo","android","apple watch","apple tv","arduino","aws","azure","drupal","esp8266","firebase","gaming console","google cloud platform","heroku","google home","ibm cloud","watson"
                            ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress"]
            #deleted skills 
            
            matches=[]
            description=description.replace("/"," ")
            filter_words=self.format_description(description)
            for unigram in word_tokenize(filter_words.lower()):
                if unigram in list_of_skills:
                    matches.append(unigram)

            for bigram in ngrams(word_tokenize(filter_words),2):
                if bigram in list_of_skills:
                    matches.append(bigram)

            for trigram in ngrams(word_tokenize(filter_words),3):
                if trigram in list_of_skills:
                    matches.append(trigram)
            return list(set(matches))
    

   
    def format_description(self,sentence:str): 
            # Split the sentence into individual words 
            
            stop_words = set(stopwords.words('english')) 
            words = sentence.split() 
                
            # Use a list comprehension to remove stop words 
            filtered_words = [word for word in words if word not in stop_words] 
                
            # Join the filtered words back into a sentence 
            return ' '.join(filtered_words)


    def parse_experience(self,description:str):
        
        years_of_experience="0"
        for sent in sent_tokenize(description):
            if "experience" in sent:
                if(len(re.findall("[0-9]|[0-9][0-9]",sent))>0):
                    experience= [int(yr) for yr in re.findall("[0-9]|[0-9][0-9]",sent) ]
                    years_of_experience= f"{min(experience)} - {max(experience)} years"

                break
                


        return years_of_experience

if __name__ =="__main__":
    #link="https://ca.indeed.com/"
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
    
    look_for_job=scrapejob("indeed") 
    look_for_job.connect()
    look_for_job.search_job("software engineer")
    look_for_job.scrape_job_data()