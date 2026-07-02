import re
import pandas as  pd
from sentence_transformers import SentenceTransformer,util
from docx import Document
from datetime import datetime

date_format = "%Y-%m-%d"

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
redrob = candidate['redrob_signals']
si=[]
dic = {
     "profile_completeness_score":0.15,
    "signup_date":{True:0.05,False:0.02},
    "last_active_date":{True:0.05,False:0.02},
    "open_to_work_flag":0.15,
    "profile_views_received_30d":0.05,
    "applications_submitted_30d":0.05,
    "recruiter_response_rate":0.10,
    "avg_response_time_hours":0.08,
    "skill_assessment_scores":0.12,
    "connection_count":0.02,
    "endorsements_received":0.03,
    "notice_period_days":0.02,
    "expected_salary_range_inr_lpa":0.5,
    "preferred_work_mode":0.25,
    "willing_to_relocate":0.25,
    "github_activity_score":0.01,
    "search_appearance_30d":0.01,
    "saved_by_recruiters_30d":0.1,
    "interview_completion_rate":0.2,
    "offer_acceptance_rate":0.2,
    "verified_email":0.1,
    "verified_phone":0.1,
    "linkedin_connected":0.05
}



for key,values in redrob.items():
   
   if key == "skill_assessment_scores":
      total=0
      for k,v in values.item():
         total+=v
      total=total/len(values)
      total=total*dic.get(key)
   if key == "expected_salary_range_inr_lpa":
      av=0
      for k,v in values.item():
         av+=v
      av=av/2
      total+=av*dic.get(key)
   if values==True:
      total+=10*dic.get(key)
   elif type(values)==str:
      parsed_date = datetime.strptime(values, date_format)
      current_date = datetime.now()
      difference = current_date - parsed_date
      if key == 'signup_date':
       if difference>14:
           total+=difference*dic.get(key).get(True)
       else:
           total+=difference*dic.get(key).get(False)
      else:
          if difference<=3:
           total+=difference*dic.get(key).get(True)
          else:
           total+=dic.get(key).get(False)
   else:
      total+=values*dic.get(key)
   
   si.append(total)
    
      
      
    

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
candidate_data['Behaviour_Score']=si
candidate_data['Final_Score']=0.5*candidate_data["Similarity_Score"]+ 0.25*candidate_data["Skill_Score"]+0.25*candidate_data["behaviour_score"]
df = candidate_data.sort_values(by='Final_Score',ascending=False)
df.to_csv('outputs/top_candidates.csv',index=False)

print(df.head(10))

 
