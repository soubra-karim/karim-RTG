import time
import plac
import random
from pathlib import Path
import spacy
from spacy.training import Example
from tqdm import tqdm
import json
import re

#[]
#[]


def drop_overlap(data):
    new_label=[]
    r=len(data)

    for index,l in zip(range(r),data):
        #start,end,label =l[1]["entities"]
        # '(5962, 5968, ['Location'])' and '(5926, 5981, ['College Name'])'
        # '(820, 827, ['Designation'])' and '(800, 824, ['Designation'])'.
        list_of_entites = l[1]["entities"]
        safe_ent=[]
        for index_ent1,l_ent in zip(range(len(list_of_entites)),list_of_entites):
            start=l_ent[0]
            end=l_ent[1]
            label=l_ent[2]
            for index_ent2,l_ent2 in zip(range(len(list_of_entites)),list_of_entites):
                    collide=False
                    start2=l_ent2[0]
                    end2=l_ent2[1]
                    label2=l_ent2[2]
                    if index_ent1 == index_ent2:
                        continue

                    if (start < end2 and end > start2) or (start2 < end and end2 > start):
                        collide=True
                        break

                #  5962 5968
                # 5926 5981
                # if start >= start2 and end <=end2:
                #     collide=True
                # #5926 5981
                # #5962 5968
                # if start<=start2 and end >=end2:
                #     collide=True
                # if start >= start2 and start <= end2:
                #     collide=True
                #     #100 200
                #     #70 170
                # if end >= start2 and end <=end2:
                #     collide=True
                #     #100 200
                #     #150 170
                # if start >=start2 and end <=end2:
                #     collide=True
                # if start == start2 and end ==end2:
                #     collide ==True
            if not(collide):
                safe_ent.append(list_of_entites[index_ent1])
        l[1]["entities"]=safe_ent
        new_label.append(l)
        """
            for index2,l2 in zip(range(r),data[index]):
                start2,end2,label2 =l2[1]["entities"]
                    # 100  200
                    # 150 250
                collide=False
                if start >= start2 and start <= end2:
                    collide=True
                    #100 200
                    #70 170
                if end >= start2 and end <=end2:
                    collide=True
                    #100 200
                    #150 170
                if start >=start2 and end <=end2:
                    collide=True
                if start == start2 and end ==end2:
                    collide ==True
            if not(collide):
                new_label.append(data[index])
            """
        
    return new_label

def trim_entity_spans(data: list) -> list:
    """Removes leading and trailing white spaces from entity spans.

    Args:
        data (list): The data to be cleaned in spaCy JSON format.

    Returns:
        list: The cleaned data.
    """
    invalid_span_tokens = re.compile(r'\s')

    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])

    return cleaned_data
traindata = []
with open('nlp/traindata.json', 'r',encoding="utf8") as file:
    for line in file:
        try:
            
                traindata.append(json.loads(line))
        except:
            pass


        
train_data=[]

for sample in traindata:
    description = sample["content"]
    entities=[]
    if sample.get("annotation"):
        for attr in sample.get("annotation"):
              label=attr['label']
              location = attr['points'][0]
              start = location['start']
              end = location['end']+1

              entities.append((start,end,label))
    # entities=drop_overlap(entities)
    train_data.append((description,{"entities" : entities}))

train_data = trim_entity_spans(train_data)
train_data= drop_overlap(train_data)
print(train_data[0])


nlp = spacy.load('en_core_web_sm')
ner_model = nlp.get_pipe('ner')
for _, annotations in train_data:
     for ent in annotations.get('entities'):
        print(ent)
        #   input("wait")
        if len(ent[2]) > 0:
            ner_model.add_label(ent[2][0])
        
        if len(ent[2]) == 0:
            pass

disable_pipes = [pipe for pipe in nlp.pipe_names if pipe!='ner']

with nlp.disable_pipes(*disable_pipes):
    #optimizer = nlp.begin_training()
    optimizer = nlp.create_optimizer()
    for itn in range(30):
        random.shuffle(train_data)
        losses = {}

        for text, annotations in tqdm(train_data):
            doc = nlp.make_doc(text)
            
            #print(isinstance(annotations["entities"], (list, tuple)))
            #time.sleep(3)
            ex = Example.from_dict(doc,annotations)
            losses = nlp.update(
                [ex],
                drop=0.5,
                sgd=optimizer
                )
        print(losses)

test = "karim soubra toronto metropolitan university"

doc = nlp(test)

for ent in doc.ents:
     print(ent.label_,ent.text)

nlp.meta["name"] = "res_parser"

nlp.to_disk("C:/Users/karim/OneDrive/Desktop/capstone/resume_final/nlp")

nlptest = spacy.load("C:/Users/karim/OneDrive/Desktop/capstone/resume_final/nlp")

print([pipe for pipe in nlptest.pipe_names])