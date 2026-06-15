#  Job Recommendation System

An NLP-powered job recommendation engine that matches users to relevant job postings based on their skills, using TF-IDF vectorization and cosine similarity.

---

##  Overview

Given a user's skill set, this system recommends the most relevant job postings from a dataset of 1,167 jobs across 5 categories. It also provides a **skill gap analysis** that shows which required skills the user already has, which are missing, and which extras they bring to the table.

### Pipeline

```
Raw CSV → EDA → Preprocessing → NLP (TF-IDF) → Cosine Similarity → Recommendations
```

---

##  Dataset

| File | Description |
|------|-------------|
| `all_job_post.csv` | Raw input — 1,167 job postings with titles, descriptions, skill sets, and categories |
| `all_job_post_cleaned.csv` | Output — cleaned and feature-enriched version of the dataset |

### Dataset Structure

| Column | Description |
|--------|-------------|
| `job_id` | Unique job identifier |
| `category` | Job category (e.g., IT, HR, Finance) |
| `job_title` | Title of the job posting |
| `job_description` | Full text description |
| `job_skill_set` | Required skills (stored as a list string) |

---

##  Project Structure

```
job_recommendation_system.ipynb   # Main notebook
all_job_post.csv                  # Input dataset
all_job_post_cleaned.csv          # Cleaned output dataset (generated)
category_distribution.png         # EDA plot
top_job_titles.png                # EDA plot
text_length_analysis.png          # EDA plot
skill_count_analysis.png          # EDA plot
top_skills_overall.png            # EDA plot
skills_by_category.png            # EDA plot
similarity_heatmap.png            # Cosine similarity heatmap
skill_gap.png                     # Skill gap bar chart
recommendations_*.png             # Recommendation score charts
```

---

##  Installation & Requirements

### Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab

### Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn nltk
```

### NLTK Downloads (run once)

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')
```

---

##  Usage

### 1. Clone / download the repository and place `all_job_post.csv` in the same directory as the notebook.

### 2. Run the notebook end-to-end, or use the core functions directly:

```python
# Get top 5 job recommendations for a set of skills
recs = recommend_jobs(
    user_skills_raw="Python, machine learning, SQL, NLP, TensorFlow",
    top_n=5
)
print(recs[['job_title', 'category', 'match_pct']])
```

### 3. Filter recommendations by category:

```python
recs = recommend_jobs(
    user_skills_raw="financial analysis, budgeting, Excel, CPA",
    top_n=5,
    filter_category="FINANCE"
)
```

### 4. Run a skill gap analysis on a recommended job:

```python
top_job = df[df['job_id'] == recs.iloc[0]['job_id']].iloc[0]
gap = skill_gap_analysis("Python, SQL, machine learning", top_job)

print(f"Match: {gap['match_pct']}%")
print(f"Matched : {gap['matched']}")
print(f"Missing : {gap['missing']}")
```

---

##  How It Works

### 1. Preprocessing

- Lowercasing, special character removal, whitespace normalization
- Tokenization, stopword removal, and lemmatization (via NLTK)
- Skill strings are parsed from list-formatted column values

### 2. Feature Engineering

A **weighted combined feature** is constructed for each job:

```
combined = skills × 3  +  title × 2  +  description × 1
```

Skills are weighted highest because they are the most direct signal for matching.

### 3. TF-IDF Vectorization

```python
TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),   # unigrams and bigrams
    min_df=2,
    max_df=0.85,
    sublinear_tf=True     # log-scale term frequencies
)
```

### 4. Cosine Similarity Matching

The user's skill input is transformed with the same vectorizer, and cosine similarity is computed against all job vectors. Jobs are ranked by score and the top-N are returned.

### 5. Skill Gap Analysis

A set comparison between the user's skills and a job's required skills produces:
- **Matched** — skills the user already has
- **Missing** — skills required by the job that the user lacks
- **Extra** — skills the user has beyond the job's requirements

---

##  Exploratory Data Analysis

The notebook generates 8 EDA visualizations:

| Plot | Description |
|------|-------------|
| Category Distribution | Bar + pie chart of job postings per category |
| Top Job Titles | Top 15 most frequent job titles |
| Text Length Analysis | Histograms of word/character counts in descriptions and titles |
| Skill Count Analysis | Distribution of skills per posting; avg by category |
| Top 20 Skills Overall | Most in-demand skills across all categories |
| Skills by Category | Top 10 skills per individual category |
| Similarity Heatmap | Cosine similarity among a 30-job sample |
| Recommendation Charts | Bar charts of similarity scores for each test query |

---

##  Example Test Cases

Three built-in test cases demonstrate the system:

| Test | Input Skills | Filter |
|------|-------------|--------|
| IT/ML | Python, machine learning, SQL, NLP, TensorFlow | None |
| HR | Talent acquisition, employee relations, payroll, SHRM | None |
| Finance | Financial analysis, budgeting, Excel, risk management, CPA | FINANCE only |

---

##  Output

The recommendation function returns a ranked DataFrame:

| Column | Description |
|--------|-------------|
| `job_id` | Job identifier |
| `category` | Job category |
| `job_title` | Job title |
| `skills_list` | Required skills |
| `similarity_score` | Raw cosine similarity (0–1) |
| `match_pct` | Similarity as a percentage string |

---

##  Summary

| Item | Detail |
|------|--------|
| Dataset | 1,167 jobs × 5 categories |
| NLP Model | TF-IDF (5,000 features, bigrams, sublinear TF) |
| Similarity Metric | Cosine Similarity |
| Key Features | Top-N recommendations, category filter, skill gap analysis, EDA visualizations |
