# import sys
import os
import requests
import urllib.parse
import streamlit as st
import pandas as pd
import sqlite3

curr_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(curr_dir, ".."))
# from RSubscribeSummarizer.data.model import RSSHubFeedEntry, RSSHubFeedSource  # noqa

API_ROOT_PATH = "/api"
API_REQUEST_ROOT = "http://api:8000"
DATABASE_PATH = os.path.join(curr_dir, "../..", "database.db")

st.title("RSS Feed by Source")


@st.cache_data
def get_feed_sources() -> list[dict]:
    return requests.get(
        f"{urllib.parse.urljoin(API_REQUEST_ROOT, 'feed_sources')}"
    ).json()


feed_sources = {source["name"]: source["title"] for source in get_feed_sources()}

rss_source_name = st.selectbox(
    "Source", feed_sources.keys(), format_func=lambda x: feed_sources[x]
)


@st.cache_data(ttl=600)
def get_feed_sources_by_source_name(rss_source_name: str) -> pd.DataFrame:
    """
    TODO: limit, order by, asc/desc
    """
    conn = sqlite3.connect(DATABASE_PATH)
    query = f"""
    SELECT 
        *
    FROM 
        RSSHubFeedEntry 
    WHERE
        RSSHubFeedEntry.rss_source = '{rss_source_name}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.dataframe(get_feed_sources_by_source_name(rss_source_name))
