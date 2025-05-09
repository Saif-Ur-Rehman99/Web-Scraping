import streamlit as st     # type: ignore
import pandas as pd
import tempfile
import os
from linkedin_scrapper import scrape_google_links 

# Page config
st.set_page_config(page_title="Google Scraper Chat", page_icon="🔍", layout="wide")

# Sidebar history
st.sidebar.title("History")
if "history" not in st.session_state:
    st.session_state.history = []

# Title
st.title("LinkedIn Scraper")
st.markdown("Type your query below to get LinkedIn links in a downloadable CSV format.")

# Input section
with st.container():
    query = st.text_input(" ", placeholder='e.g. inurl:linkedin.com/in "enterprise" "@gmail.com" "France"', label_visibility="collapsed")

with st.container():
    col_num, col_btn = st.columns([7, 3])
    with col_num:
        num = st.number_input(" ", min_value=1, max_value=50, value=10, label_visibility="collapsed")
    with col_btn:
        scrape = st.button("🚀 Scrape Now")

# Scraping handler
if scrape and query.strip():
    st.session_state.history.append((query, num))
    with st.spinner("Scraping Google..."):
        links = scrape_google_links(query, num)

    if links:
        st.success(f"✅ Found {len(links)} links.")
        df = pd.DataFrame(links, columns=["link", "email"])
        st.dataframe(df, use_container_width=True)

        tmp_download = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(tmp_download.name, index=False)
        with open(tmp_download.name, "rb") as f:
            st.download_button("📥 Download CSV", f, file_name="google_links.csv", mime="text/csv")
        os.unlink(tmp_download.name)
    else:
        st.warning("⚠️ No links found.")

# Sidebar history display
with st.sidebar:
    if st.session_state.history:
        for i, (q, n) in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.markdown(f"**{i}.** `{q}`<br><small>{n} results</small>", unsafe_allow_html=True)
    else:
        st.info("No queries yet.")

# Styling
st.markdown("""
<style>
    .element-container:has(.stTextInput), .element-container:has(.stNumberInput) {
        margin-top: 0 !important;
    }
    .stButton > button {
        width: 100%;
        height: 100%;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)
