import streamlit as st
from search_engine import search

st.set_page_config(page_title="CNN Search Engine", layout="wide")
st.title("🔍 CNN News Search Engine")

query = st.text_input("Enter your search query:")

if query:
    with st.spinner("Searching..."):
        results = search(query, top_k=10)

    st.markdown(f"### Top results for: *{query}*")
    for r in results:
        title = str(r['title']).strip().replace('\n', ' ')
        st.markdown(f"#### [{title}]({r['source_url']})")
        st.markdown(f"Category: *{r['cate']}* | Score: `{r['score']}`")
        st.write("---")
