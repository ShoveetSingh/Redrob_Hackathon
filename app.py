import re
import pandas as  pd
from sentence_transformers import SentenceTransformer,util
from docx import Document


model=SentenceTransformer('all-MiniLM-L6-v2')

data = Document('datasets/job_description.docx')

job_data=''
c=False
job_skill=[]
skill=''

for p in data.paragraphs:
    if p.style.name.startswith('Heading'):
        text = p.text.strip()
        if 'Things you absolutely need' in text | "Things we'd like you to have but won't reject you for" in text:
          skill+=p.text+' '
        if 'Things we explicitly do NOT want' in text:
         c=True
        else:
           c=False
        if c==False:
         job_data+=p.text+' '


job_skill = re.findall(r"[A-Za-z0-9+#.-]+(?:\s+[A-Za-z0-9+#.-]+)?", skill)

stop_words = {
    "things", "absolutely", "need", "like", "would", "want",
    "have", "for", "the", "a", "an", "to", "of", "on", "in",
    "at", "by", "from", "with", "without", "or", "and", "as",
    "is", "are", "be", "been", "being", "that", "this", "these",
    "those", "it", "its", "their", "them", "they", "you", "your",
    "we", "our", "us", "i", "me", "my",
    "production", "experience", "strong", "really", "yes",
    "care", "handled", "designing", "deployed", "users",
    "specific", "similar", "again", "matter", "operational",
    "does", "hands", "hand", "thought", "painful",
    "role", "never", "about", "how", "if", "don't",
    "doesn't", "won't", "reject", "prior", "background",
    "contributions", "space", "products", "model", "models",
    "systems", "system", "frameworks", "framework",
    "ranking", "evaluation", "test", "tests", "quality",
    "code", "tech", "real", "user", "using"
}

job_des=set()



for j in job_skill:
   if j.lower() in stop_words:
      continue
   else:
      job_des.add(j.lower())


emb1 = model.encode(job_data)

candidate_data=pd.read_json('datasets/candidates.jsonl',lines=True)

list=[]
candidate=[]
incr =0
candidate_skill=[]

for row in candidate_data.itertuples(index=True):
    s=''
    sk= ''
    cand_des=set()
    for item in row:
        s+=str(item)+' '
    for skill in row.skill:
      cand_des.add(skill['name'].lower())
    res=job_des.intersection(cand_des)
    candidate_skill.append(len(job_des)/len(res))
    
    candidate.append(s)
    
emb2 = model.encode(candidate,
                    batch_size=64,
                    show_progress_bar=True,
                    )

similarity = util.cos_sim(emb1,emb2)

list = [x.item() for x in similarity[0]]

candidate_data['Similarity_Score']=list
candidate_data['Skill_Score']=candidate_skill


#df = candidate_data.sort_values(by='Similarity',ascending=False)

#print(df.head(100))

 
