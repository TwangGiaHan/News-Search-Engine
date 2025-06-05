# app.py (Streamlit Version)

import streamlit as st
import numpy as np
import json
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

@st.cache_data
def preprocess_text(text):
    tokens = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    tokens = [t for t in tokens if t not in stop_words]
    stemmed = [stemmer.stem(t) for t in tokens]
    return ' '.join(stemmed)

@st.cache_resource
def load_resources():
    tfidf_matrix = np.load("tfidf_matrix.npy")
    with open("metadata.json", encoding="utf-8") as f:
        metadata = json.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return tfidf_matrix, metadata, vectorizer

def search(query, top_k=10):
    tfidf_matrix, metadata, vectorizer = load_resources()
    query_proc = preprocess_text(query)
    query_vec = vectorizer.transform([query_proc]).toarray()
    scores = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_indices = scores.argsort()[-top_k:][::-1]
    results = []
    for idx in top_indices:
        results.append({
            "title": metadata[idx].get("title", "(no title)"),
            "url": metadata[idx].get("source_url", "#"),
            "cate": metadata[idx].get("cate", "unknown"),
            "score": round(scores[idx], 4)
        })
    return results

# Streamlit UI
st.set_page_config(page_title="CNN News Search", layout="wide")
st.title("📰 CNN News Search Engine")

query = st.text_input("🔍 Enter your search query:")
if query:
    with st.spinner("Searching..."):
        results = search(query)
    st.markdown(f"### 🔎 Top results for: *{query}*")
    for res in results:
        title = str(res['title']).strip().replace('\n', ' ')
        st.markdown(f"#### [{title}]({res['url']})")
        st.markdown(f"Category: *{res['cate']}* | Score: `{res['score']}`")
        st.write("---")
