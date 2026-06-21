#  Candidate Discovery AI

An AI-powered candidate ranking and discovery system built for the **INDIA RUNS Data & AI Challenge**.

This project goes beyond traditional keyword-based filtering by combining **semantic understanding**, **skills matching**, **career analysis**, and **behavioral hiring signals** to identify and rank the most suitable candidates for a given job description.

---

##  Problem Statement

Recruiters often rely on keyword matching, which can miss highly qualified candidates whose profiles do not contain exact keywords.

This project aims to build an intelligent recruitment assistant capable of:

* Understanding complex job descriptions
* Performing semantic candidate matching
* Evaluating skills and experience relevance
* Incorporating behavioral and activity signals
* Generating explainable candidate rankings

---

##  Features

### Semantic Job Matching

Uses transformer-based embeddings to understand the meaning of job descriptions and candidate profiles.

### Intelligent Candidate Ranking

Combines multiple factors into a single ranking score:

* Semantic Similarity
* Skills Alignment
* Experience Relevance
* Redrob Behavioral Signals

### Explainable Recommendations

Provides transparent scoring for every candidate.

Example:

| Metric           | Score |
| ---------------- | ----- |
| Semantic Match   | 92    |
| Skills Match     | 88    |
| Experience Match | 95    |
| Behavioral Score | 84    |
| Final Score      | 90.7  |

### Export Results

Generate ranked candidate lists in:

* CSV
* XLSX

formats for recruiter review.

---

##  Architecture

```text
Job Description
       │
       ▼
Semantic Analysis
       │
       ▼
Candidate Processing
       │
       ▼
Multi-Factor Ranking Engine
       │
       ▼
Ranked Candidates
       │
       ▼
CSV / XLSX Export
```

---

##  Ranking Methodology

The final candidate score is computed using:

```python
final_score = (
    0.50 * semantic_score +
    0.20 * skill_score +
    0.15 * experience_score +
    0.15 * behavior_score
)
```

### Semantic Score

Measures contextual similarity between:

* Job Description
* Candidate Summary
* Career History
* Skills

### Skill Score

Evaluates overlap between required and possessed skills.

### Experience Score

Measures alignment with required experience level.

### Behavioral Score

Uses Redrob behavioral indicators such as:

* Profile Completeness
* Recruiter Response Rate
* Interview Completion Rate
* Open To Work Status
* Saved By Recruiters
* Search Appearance

---

##  Tech Stack

| Component         | Technology            |
| ----------------- | --------------------- |
| Backend           | Flask                 |
| Database          | SQLite                |
| ORM               | SQLAlchemy            |
| Data Processing   | Pandas                |
| Embeddings        | Sentence Transformers |
| Similarity Search | Scikit-learn          |
| Frontend          | HTML, CSS, JavaScript |
| Export            | OpenPyXL              |

---

##  Project Structure

```text
candidate_discovery/
│
├── app.py

│
├── dataset/
│   ├── candidates.jsonl
│   └── candidate_schema.json
│
├── templates/
│   ├── index.html
│
├── outputs/
│
├── requirements.txt
└── README.md
```

---

##  Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/candidate-discovery-ai.git
cd candidate-discovery-ai
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
python app.py
```

---

##  Dataset

The project utilizes:

* Candidate Profiles
* Career History
* Skills
* Education
* Certifications
* Redrob Behavioral Signals

to build an intelligent ranking pipeline.

---

##  Demo Workflow

1. Enter Job Description
2. Load Candidate Dataset
3. Run AI Ranking Engine
4. View Ranked Candidates
5. Export Results

---

##  Future Improvements

* Multi-Agent Recruitment Pipeline
* Interview Question Generation
* Candidate Skill Gap Analysis
* Resume Parsing Support
* Real-Time Recruiter Dashboard
* LLM-Based Candidate Explanations

---

##  Team

Developed as part of the **INDIA RUNS Data & AI Challenge**.

Building the future of intelligent hiring through AI-powered candidate discovery.
