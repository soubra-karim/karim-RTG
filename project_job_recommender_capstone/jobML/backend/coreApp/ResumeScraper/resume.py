import PyPDF2
import re
import csv

import spacy
# import openai
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os


class ResumeExtractor:
    def __init__(self):

        env_path = Path(__file__).parent / '.env'

        skill_path = Path(__file__).parent / 'skills.csv'

        load_dotenv(env_path)
        OpenAI.api_key=os.getenv('OPENAI_API_KEY')
        self.client = OpenAI()
        with open(skill_path) as fp:
            render = csv.reader(fp,delimiter=",")

            data_read= [row for row in render]


        self.new_skills= [i.lower() for i in data_read[0]]
        self.resume_text=None
    def read_resume(self,text=None,path=None,unformatted=False,pdf=False):
        def remove_non_ascii_1(text):

            return ''.join(i for i in text if ord(i)<128)

        if pdf:
            resume = open(path, 'rb')

            resumepdf= PyPDF2.PdfReader(resume)
            
            text=""
            for page in resumepdf.pages:
                text+=page.extract_text()
                
                
        
        
            text2 = ' '.join(text.split())



            text3=remove_non_ascii_1(text2).replace(","," ").replace(":"," ").lower()
            if unformatted:
                return text2
            else:
                return text3
        else:
            text3=remove_non_ascii_1(text).replace(","," ").replace(":"," ").replace('\n'," ").lower()
            if unformatted:
                return text
            else:
               
                return text3
        


    #DONE
    def extract_email(self,text):
            get_email = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=0.2,
                    messages=[
                        
                        {"role": "user", "content": "Extract the email from the text. IF NO ADDRESS FOUND REPLY WITH none"},
                        
                        {"role": "user", "content": text}
                    ] 
                )
            return  get_email.choices[0].message.content
    # def extract_email(self,text):
    #     email =""
    #     for word in text.split(" "):
            
    #         if re.findall("([a-z]|.)*@[a-z]*\.(com|ca)",word):
    #             email = word
    #             break
    #     return email
    def extract_skills(self,text):
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
                            ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress","c/c++","nosql","quartus","hip" , "cuda","git","github","git/github","react.js"]

        list_of_skills.append(self.new_skills)
        skill=[]
        for word in text.split(" "):
            
            if word in list_of_skills:
                skill.append(word)

        if len(skill) == 0:
            """
                returns :
                "Skills": [Python, JavaScript, React, Django]
            """
            get_skills = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=0.2,
                    messages=[
                        
                        {"role": "user", "content": "Extract all the skills? LIST THE SKILLS IN A COMMA SEPARATED LIST.IF NOTHING FOUND REPLY WITH none"},
                        {"role": "assistant", "content": "python,javascript,react,django"},
                        {"role": "user", "content": text}
                    ] 
                )

            get_skills_response= get_skills.choices[0].message.content

            split_skills = list(set(get_skills_response.split(",")))
            
            join_skills = ",".join(split_skills)
            return join_skills
        else:
            return ",".join(list(set(skill)))
    def extract_number(self,text):
        
        
        phone_number= re.findall("\(\d+\)\s\d+-\d+",text )

        if not(phone_number):
            phone_number= re.findall("\d+-\d+-\d+",text )

        if phone_number:
            return phone_number
        else:
            return ""
    

    def extract_address(self,text):
            get_address = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=0.2,
                    messages=[
                        
                        {"role": "user", "content": "Extract the house address from the text. IF NO ADDRESS FOUND REPLY WITH none"},
                        
                        {"role": "user", "content": text}
                    ] 
                )
            return  get_address.choices[0].message.content
    #DONE
    def extract_experience(self,text):
        """
        Returns:
         [
                {
                    "Company Name": "ABC Corp",
                    "Job Title": "Software Developer",
                    "Start Date": "2020-01",
                    "End Date": "2022-12",
                    "job_description : " ... "
                },
                {
                    "Company Name": "DEF Technologies",
                    "Job Title": "Junior Developer",
                    "Start Date": "2018-06",
                    "End Date": "2020-01",
                    "job_description : " ... "
                }
            ],
        """
        job_data=[]
        job_description = ""

        # model="gpt-4-turbo-preview",
        get_job_titles = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            temperature=0.2,
            messages=[
                
                {"role": "user", "content": "what are the different job titles the person has? Only list the job titles separated by comma if needed. IF NOTHING FOUND REPLY WITH none"},
                {"role": "assistant", "content": "software engineer, power and performance engineer, silicon design engineer"},
                {"role": "user", "content": text}
            ] 
        )

        job_titles_response= get_job_titles.choices[0].message.content

        for job_titles in job_titles_response.split(","):

            get_job_desc = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                messages=[
                    
                    {"role": "user", "content": f"what responsibilities did the {job_titles} have in the text? ONLY LIST THE responsibilities without any formatting.IF NOTHING FOUND REPLY WITH none"},
                    
                    {"role": "user", "content": text}
                ]  
            )
            job_desc = get_job_desc.choices[0].message.content

            get_company_names = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                messages=[
                    
                    {"role": "user", "content": f"what company did the person work for as a {job_titles}? only list the company name. IF NOTHING FOUND REPLY WITH none"},
                    {"role": "assistant", "content": "Intel,AMD,IBM,Google"},
                    {"role": "user", "content": text}
                ]  
            )

            company_name = get_company_names.choices[0].message.content
            get_start_date = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                max_tokens=60,
                messages=[
                    
                    {"role": "user", "content": f"what is the starting date of the person's role as {job_titles}? ONLY LIST THE START DATE. IF NOTHING FOUND REPLY WITH none"},
                    {"role": "assistant", "content": "year-month-day"},
                    {"role": "user", "content": text}
                ]   
            )
            start_date_response = get_start_date.choices[0].message.content

            get_end_date = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                     temperature=0.2,
                max_tokens=60,
                messages=[
                    
                    {"role": "user", "content": f"what is the end date of the person's role as {job_titles}? ONLY LIST THE END DATE. IF NOTHING FOUND REPLY WITH none"},
                    {"role": "assistant", "content": "year-month-day"},
                    {"role": "user", "content": text}
                ]   
            )
            end_date_response = get_end_date.choices[0].message.content

            #   "start_date": start_date_response,
            #         "end_date ": end_date_response,
            data = {
                    "company_name": company_name,
                    "job_title":job_titles,
                  
                    "job_description" : job_desc
            }
            job_data.append(data)

        return job_data
    def use_nlp(self,text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        first_name=""
        last_name=""
        for token in doc:
                # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                #         token.shape_, token.is_alpha, token.is_stop)
                if first_name=="" and token.pos_=="PROPN":
                    first_name=token.text
                    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                    #     token.shape_, token.is_alpha, token.is_stop)
                elif last_name=="" and token.pos_=="PROPN":
                    last_name=token.text
              
                    break
        return [first_name,last_name]
    
    def extract_name(self,text):
            get_name = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                     temperature=0.2,
                max_tokens=60,
                messages=[
                    
                    {"role": "user", "content": f"Extract the name from this text. ONLY LIST THE NAME. IF NOTHING FOUND REPLY WITH none"},
                    {"role": "assistant", "content": "year-month-day"},
                    {"role": "user", "content": text}
                ]   
            )
            name_response = get_name.choices[0].message.content

            return name_response    

    def extract_education(self,text):
            """
            Returns:
            "education_data": [
                    {
                        "School": "XYZ University",
                        "Degree": "MSc in Computer Science",
                        "Start Date": "2020",
                        "End Date": "2022"
                    },
                    {
                        "School": "ABC College",
                        "Degree": "BSc in Software Engineering",
                        "Start Date": "2016",
                        "End Date": "2020"
                    }
                ]
            """
            education_data=[]
            get_degrees = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                max_tokens=60,
                messages=[
                    
                    {"role": "user", "content": f"extract the different university or college degrees this person has. ONLY LIST THE DEGREE NAME. If there are multiple degrees use a comma to seperate them.IF NOTHING FOUND REPLY WITH none"},
                    
                    {"role": "user", "content": text}
                ]   
            )
            get_degrees_response = get_degrees.choices[0].message.content

            for degrees in get_degrees_response.split(','):

                
                get_start_date = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=0.2,
                    max_tokens=60,
                    messages=[
                        
                        {"role": "user", "content": f"what is the starting date of the person's {degrees} degree? ONLY LIST THE START DATE.REPLY WITH the format year-month-day. IF NOTHING FOUND REPLY WITH none"},
                        {"role": "assistant", "content": "year-month-day"},
                        {"role": "user", "content": text}
                    ]   
                )
                start_date_response = get_start_date.choices[0].message.content

                get_end_date = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                        temperature=0.2,
                    max_tokens=60,
                    messages=[
                        
                        {"role": "user", "content": f"what is the starting date of the person's {degrees} degree? ONLY LIST THE END DATE. REPLY WITH the format year-month-day. IF NOTHING FOUND REPLY WITH none"},
                        {"role": "assistant", "content": "year-month-day"},
                        {"role": "user", "content": text}
                    ]   
                )
                end_date_response = get_end_date.choices[0].message.content

                get_school = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                        temperature=0.2,
                    max_tokens=60,
                    messages=[
                        
                        {"role": "user", "content": f"in what school did the person get the {degrees} degree at ? ONLY NAME THE SCHOOL. IF NOTHING FOUND REPLY WITH none"},
                        {"role": "assistant", "content": "year-month-day"},
                        {"role": "user", "content": text}
                    ]   
                )
                get_school_response = get_school.choices[0].message.content

                if start_date_response == "none":
                     start_date_response="2020-9-23"
                #"start_date" : start_date_response , "end_date" : end_date_response
                data = {"school_name" : get_school_response , "degree" : degrees }
                education_data.append(data)

            return education_data

        
    def extract_all(self,text=None,filename=None,ispdf=True):
        if filename!=None:
            text= self.read_resume(path=filename,pdf=ispdf)
        elif text !=None:
            text= self.read_resume(text=text,pdf=ispdf)
        
        #data = {"Educations" : self.extract_education(text) , "Work Experiences" : self.extract_experience(text) ,"Skills" : self.extract_skills(text),"address" : self.extract_address(text)}
        data = {"educations" : self.extract_education(text) , "work_experiences" : self.extract_experience(text) ,"resume_skills" : self.extract_skills(text)}
        return data
if __name__ == "__main__":
    resextractor = ResumeExtractor()
    text = resextractor.read_resume("./karim_soubra_resume.pdf")
    print(resextractor.extract_address(text))