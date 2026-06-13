# Replace your current DATA_PATH section with this

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "all_job_post.csv")

REQUIRED_COLUMNS = {
    "job_id",
    "category",
    "job_title",
    "job_skill_set"
}

# Inside build_engine(), replace:
# df = pd.read_csv(DATA_PATH)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}\n"
        "Make sure all_job_post.csv is in the same folder as app.py"
    )

if os.path.getsize(DATA_PATH) == 0:
    raise ValueError(
        "all_job_post.csv exists but is empty (0 bytes)."
    )

try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except pd.errors.EmptyDataError:
    raise ValueError(
        "CSV file contains no readable columns. "
        "Check whether the uploaded file is empty or corrupted."
    )

missing_cols = REQUIRED_COLUMNS - set(df.columns)
if missing_cols:
    raise ValueError(
        f"Missing required columns: {missing_cols}\n"
        f"Available columns: {list(df.columns)}"
    )
