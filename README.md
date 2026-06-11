# Job Recommendation System

This repository contains a Streamlit job recommendation app using TF-IDF and cosine similarity.

## Ready to deploy

The app is deployable to:

- **Streamlit Community Cloud**
- **Hugging Face Spaces (Streamlit)**

## Files

- `app.py` — main Streamlit application
- `requirements.txt` — Python dependencies
- `all_job_post.csv` — dataset used by the app

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to https://share.streamlit.io/
3. Click `New app` and connect your GitHub repo.
4. Select the repository, branch, and `app.py` as the main file.
5. Deploy.

## Deploy on Hugging Face Spaces

1. Push this repository to GitHub (or upload it directly to Hugging Face).
2. Go to https://huggingface.co/spaces
3. Create a new Space.
4. Choose `Streamlit` as the SDK.
5. Connect your GitHub repo or upload the repository contents.
6. Make sure `requirements.txt` is present.
7. Start the Space.

## Notes

- `requirements.txt` already includes `streamlit`, `nltk`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`, and `scipy`.
- The app downloads NLTK data on first startup and caches it locally.
- Keep `all_job_post.csv` in the repository so the app can load the dataset on deploy.
