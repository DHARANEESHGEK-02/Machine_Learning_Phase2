"""
Job Recommendation System — Streamlit App
Extracted from job_recommendation_system.ipynb
"""

import ast
import re
import os
import sys

BASE_DIR = os.path.dirname(__file__)
os.environ.setdefault("MPLCONFIGDIR", os.path.join(BASE_DIR, ".matplotlib-cache"))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Job Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── NLTK bootstrap (runs once) ────────────────────────────────────────────────
import nltk

NLTK_DATA_PATH = os.path.join(BASE_DIR, ".nltk_data")
os.makedirs(NLTK_DATA_PATH, exist_ok=True)
if NLTK_DATA_PATH not in nltk.data.path:
    nltk.data.path.insert(0, NLTK_DATA_PATH)

@st.cache_resource(show_spinner="Downloading NLTK data…")
def _download_nltk():
    for pkg in ["stopwords", "punkt", "punkt_tab", "wordnet", "omw-1.4"]:
        nltk.download(pkg, download_dir=NLTK_DATA_PATH, quiet=True)

_download_nltk()

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0b1528 0%, #121f3a 48%, #0f1720 100%);
    min-height: 100vh;
}

/* Glass card */
.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 28px rgba(0,0,0,0.28);
}

/* Hero */
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    line-height: 1.2;
}
.hero-sub {
    text-align: center;
    color: rgba(255,255,255,0.6);
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-card {
    flex: 1;
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
}
.metric-val { font-size: 2rem; font-weight: 700; color: #a78bfa; }
.metric-label { font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 0.3rem; }

/* Result rows */
.result-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-left: 4px solid #a78bfa;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s;
}
.result-card:hover { background: rgba(255,255,255,0.08); }
.result-rank { font-size: 1.4rem; font-weight: 700; color: #a78bfa; }
.result-title { font-size: 1.05rem; font-weight: 600; color: #f0f0f0; }
.result-cat {
    display: inline-block;
    background: rgba(96,165,250,0.2);
    border: 1px solid rgba(96,165,250,0.4);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    color: #60a5fa;
    margin: 4px 4px 0 0;
}
.score-bar-bg {
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
    height: 6px;
    margin-top: 8px;
}
.score-bar-fill {
    height: 6px;
    border-radius: 4px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    width: 100%;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Inputs */
.stTextArea textarea, .stSelectbox select {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Tab header */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.6); }
.stTabs [aria-selected="true"] {
    background: rgba(167,139,250,0.3) !important;
    color: white !important;
    border-radius: 8px;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.1) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Data helpers ──────────────────────────────────────────────────────────────

DATA_PATH = os.path.join(BASE_DIR, "all_job_post.csv")

def parse_skills(skill_str):
    try:
        return ast.literal_eval(skill_str)
    except Exception:
        return [s.strip().strip("'[]") for s in str(skill_str).split(",")]


def skills_to_string(skills_list):
    cleaned = [re.sub(r"[^a-z\s]", "", s.lower().strip()) for s in skills_list]
    return " ".join([c for c in cleaned if c.strip()])


@st.cache_resource(show_spinner="🔧 Building recommendation engine…")
def build_engine():
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    def clean_text(text):
        text = str(text).lower()
        text = re.sub(r"[^a-z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(t) for t in tokens
                  if t not in stop_words and len(t) > 2]
        return " ".join(tokens)

    df = pd.read_csv(DATA_PATH)

    # Parse & clean
    df["skills_list"]       = df["job_skill_set"].apply(parse_skills)
    df["skill_count"]       = df["skills_list"].apply(len)
    df["skills_string"]     = df["skills_list"].apply(skills_to_string)
    df["clean_description"] = df["job_description"].apply(clean_text)
    df["clean_title"]       = df["job_title"].apply(clean_text)

    # Weighted combined features (skills×3, title×2, desc×1)
    df["combined_features"] = (
        df["skills_string"]     + " " +
        df["skills_string"]     + " " +
        df["skills_string"]     + " " +
        df["clean_title"]       + " " +
        df["clean_title"]       + " " +
        df["clean_description"]
    )

    # TF-IDF
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.85,
        sublinear_tf=True,
    )
    tfidf_matrix = tfidf.fit_transform(df["combined_features"])

    return df, tfidf, tfidf_matrix


def extract_user_skills(raw_input: str) -> str:
    skills = [s.strip().lower() for s in raw_input.split(",") if s.strip()]
    cleaned = [re.sub(r"[^a-z\s]", "", s) for s in skills]
    return " ".join(cleaned)


def recommend_jobs(user_skills_raw, top_n, filter_category, df, tfidf, tfidf_matrix):
    if not user_skills_raw.strip():
        return None, "Please provide at least one skill."

    user_vector_str = extract_user_skills(user_skills_raw)

    if not user_vector_str.strip():
        return None, "No recognisable skills found after cleaning."

    user_vec = tfidf.transform([user_vector_str])

    if filter_category and filter_category != "All Categories":
        mask       = (df["category"].str.upper() == filter_category.upper()).values
        indices    = np.where(mask)[0]
        sub_matrix = tfidf_matrix[indices]
        sub_df     = df.iloc[indices].reset_index(drop=True)
    else:
        sub_matrix = tfidf_matrix
        sub_df     = df.reset_index(drop=True)

    similarities = cosine_similarity(user_vec, sub_matrix).flatten()
    top_indices  = similarities.argsort()[-top_n:][::-1]

    results = sub_df.iloc[top_indices][
        ["job_id", "category", "job_title", "skills_list"]
    ].copy()
    results["similarity_score"] = similarities[top_indices].round(4)
    results["match_pct"]        = (results["similarity_score"] * 100).round(1).astype(str) + "%"
    results = results.reset_index(drop=True)
    results.index += 1

    return results, user_vector_str


# ─── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("##  Settings")
    st.markdown("---")

    top_n = st.slider(" Number of Results", min_value=3, max_value=20, value=5, step=1)

    try:
        df_meta, _, _ = build_engine()
        categories = ["All Categories"] + sorted(df_meta["category"].unique().tolist())
    except Exception:
        categories = ["All Categories"]

    filter_cat = st.selectbox("🗂 Filter by Category", categories)

    st.markdown("---")
    st.markdown("###  Example Skills")
    examples = {
        " IT / ML":    "Python, machine learning, SQL, data analysis, TensorFlow, NLP",
        " HR":         "talent acquisition, employee relations, performance management, payroll, SHRM",
        " Finance":    "financial analysis, budgeting, forecasting, Excel, risk management, CPA",
        " Sales":      "B2B sales, CRM, Salesforce, cold calling, lead generation",
        " Biz Dev":    "business development, strategic partnerships, market research, negotiation",
    }
    for label, skills in examples.items():
        if st.button(label, key=f"ex_{label}"):
            st.session_state["skills_input"] = skills

    st.markdown("---")
    st.markdown("<p style='color:rgba(255,255,255,0.3);font-size:0.75rem;text-align:center;'>Powered by TF-IDF · Cosine Similarity</p>", unsafe_allow_html=True)


# ─── Main ──────────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div style='padding: 2.5rem 0 1.5rem;'>
  <div class='hero-title'> Job Recommendation System</div>
  <div class='hero-sub'>Enter your skills and discover perfectly matched job opportunities</div>
</div>
""", unsafe_allow_html=True)

# Load engine
with st.spinner("Loading recommendation engine…"):
    try:
        df, tfidf, tfidf_matrix = build_engine()
        engine_ok = True
    except FileNotFoundError:
        st.error(f"❌ Dataset not found at `{DATA_PATH}`. Place `all_job_post.csv` in the same folder as `app.py`.")
        engine_ok = False
    except Exception as exc:
        st.error(f"❌ Engine error: {exc}")
        engine_ok = False

if engine_ok:
    # Quick stats
    cats    = df["category"].nunique()
    total   = len(df)
    avg_sk  = df["skill_count"].mean()

    st.markdown(f"""
    <div class='metric-row'>
      <div class='metric-card'><div class='metric-val'>{total:,}</div><div class='metric-label'>Job Postings</div></div>
      <div class='metric-card'><div class='metric-val'>{cats}</div><div class='metric-label'>Categories</div></div>
      <div class='metric-card'><div class='metric-val'>{avg_sk:.1f}</div><div class='metric-label'>Avg Skills / Job</div></div>
    </div>
    """, unsafe_allow_html=True)

# ─── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("###  Enter Your Skills")
st.markdown("<p style='color:rgba(255,255,255,0.5);font-size:0.9rem;'>Separate multiple skills with commas</p>", unsafe_allow_html=True)

default_skills = st.session_state.get("skills_input", "")
user_skills = st.text_area(
    label="Skills",
    value=default_skills,
    height=120,
    placeholder="e.g. Python, machine learning, SQL, data analysis, TensorFlow",
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit = st.button(" Find My Jobs", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Results ───────────────────────────────────────────────────────────────────
if submit and engine_ok:
    if not user_skills.strip():
        st.warning(" Please enter at least one skill before searching.")
    else:
        with st.spinner("Finding best matches…"):
            results, processed_query = recommend_jobs(
                user_skills, top_n,
                None if filter_cat == "All Categories" else filter_cat,
                df, tfidf, tfidf_matrix,
            )

        if results is None:
            st.error(f" {processed_query}")
        else:
            st.markdown(f"""
            <div style='background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);
                border-radius:12px;padding:0.8rem 1.2rem;margin-bottom:1.5rem;'>
              <span style='color:#34d399;font-weight:600;'> Processed query:</span>
              <span style='color:rgba(255,255,255,0.7);'> {processed_query}</span>
            </div>
            """, unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs([" Recommendations", " Score Chart", " Full Table"])

            # ── Tab 1 : Cards ────────────────────────────────────────────────
            with tab1:
                st.markdown(f"### Top {len(results)} Matches")
                for rank, row in results.iterrows():
                    score = row["similarity_score"]
                    bar_w = min(int(score * 400), 100)
                    color = ("#34d399" if score >= 0.25
                             else "#60a5fa" if score >= 0.15
                             else "#a78bfa")
                    skills_preview = ", ".join(row["skills_list"][:6]) + ("…" if len(row["skills_list"]) > 6 else "")

                    st.markdown(f"""
                    <div class='result-card'>
                      <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <div class='result-rank'>#{rank}</div>
                        <div style='color:{color};font-weight:700;font-size:1.1rem;'>{row['match_pct']}</div>
                      </div>
                      <div class='result-title' style='margin-top:6px;'>{row['job_title']}</div>
                      <span class='result-cat'>{row['category']}</span>
                      <div style='color:rgba(255,255,255,0.4);font-size:0.8rem;margin-top:6px;'>
                          {skills_preview}
                      </div>
                      <div class='score-bar-bg'>
                        <div class='score-bar-fill' style='width:{bar_w}%;background:linear-gradient(90deg,{color},{color}99);'></div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Tab 2 : Chart ────────────────────────────────────────────────
            with tab2:
                st.markdown("### Similarity Score Breakdown")
                fig, ax = plt.subplots(figsize=(9, 4))
                fig.patch.set_facecolor("#1a1a2e")
                ax.set_facecolor("#16213e")

                labels  = [f"#{r}  {row['job_title'][:35]}" for r, row in results.iterrows()]
                scores  = results["similarity_score"].tolist()
                colors  = plt.cm.plasma(np.linspace(0.3, 0.85, len(scores)))

                bars = ax.barh(labels[::-1], scores[::-1], color=colors[::-1], height=0.6, edgecolor="none")

                for bar, val in zip(bars, scores[::-1]):
                    ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
                            f"{val:.3f}", va="center", ha="left",
                            fontsize=9, color="white")

                ax.set_xlabel("Cosine Similarity", color="white", fontsize=10)
                ax.set_title("Job Match Scores", color="white", fontsize=12, fontweight="bold")
                ax.tick_params(colors="white", labelsize=8)
                for spine in ax.spines.values():
                    spine.set_color((1.0, 1.0, 1.0, 0.16))
                ax.set_xlim(0, min(max(scores) * 1.35, 1.0))
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

            # ── Tab 3 : Table ────────────────────────────────────────────────
            with tab3:
                st.markdown("### Full Result Table")
                display_df = results[["job_id", "category", "job_title", "similarity_score", "match_pct"]].copy()
                display_df.columns = ["Job ID", "Category", "Title", "Score", "Match %"]
                st.dataframe(display_df, use_container_width=True)

# ─── EDA section ───────────────────────────────────────────────────────────────
if engine_ok:
    st.markdown("---")
    with st.expander(" Dataset Overview", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Jobs per Category")
            cat_counts = df["category"].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6, 3.5))
            fig2.patch.set_facecolor("#1a1a2e")
            ax2.set_facecolor("#16213e")
            colors2 = plt.cm.plasma(np.linspace(0.2, 0.9, len(cat_counts)))
            ax2.barh(cat_counts.index[::-1], cat_counts.values[::-1], color=colors2, edgecolor="none")
            ax2.set_xlabel("Count", color="white")
            ax2.tick_params(colors="white", labelsize=8)
            ax2.spines[:].set_color("#333")
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

        with col2:
            st.markdown("#### Skills Distribution")
            fig3, ax3 = plt.subplots(figsize=(6, 3.5))
            fig3.patch.set_facecolor("#1a1a2e")
            ax3.set_facecolor("#16213e")
            ax3.hist(df["skill_count"], bins=20, color="#a78bfa", edgecolor="none", alpha=0.85)
            ax3.axvline(df["skill_count"].mean(), color="#60a5fa", linestyle="--",
                        label=f"Mean: {df['skill_count'].mean():.1f}")
            ax3.set_xlabel("Skills per Job", color="white")
            ax3.set_ylabel("Frequency", color="white")
            ax3.tick_params(colors="white", labelsize=8)
            ax3.spines[:].set_color("#333")
            ax3.legend(facecolor="#1a1a2e", edgecolor="#555", labelcolor="white", fontsize=8)
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)
