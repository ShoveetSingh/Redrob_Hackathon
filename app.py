from flask import Flask
import pandas as  pd
from sentence_transformers import SentenceTransformer,util
from docx import Document


model=SentenceTransformer('all-MiniLM-L6-v2')

data = Document('datasets/job_description.docx')

job_data=''

for p in data.paragraphs:
    job_data+=p.text+' '

emb1 = model.encode(job_data)

candidate_data=pd.read_json('datasets/candidates.jsonl',lines=True)

list=[]
for row in candidate_data.itertuples(index=True):

    s=''
    for item in row:
        s+=str(item)+' '
    emb2 = model.encode(s)
    similarity = util.cos_sim(emb1,emb2).item()
    if similarity >= 0.5:
        list.append(similarity)

candidate_data['Similarity']=list

df = candidate_data.sort_values(by='Similarity',ascending=False)

print(df.head(100))
