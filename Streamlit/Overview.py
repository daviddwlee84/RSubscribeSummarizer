# import sys
import os
import requests
import urllib.parse
import streamlit as st
import pandas as pd

curr_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(curr_dir, ".."))
# from RSubscribeSummarizer.data.model import RSSHubFeedEntry, RSSHubFeedSource  # noqa

API_ROOT_PATH = "/api"
API_REQUEST_ROOT = "http://api:8000"
DATABASE_PATH = os.path.join(curr_dir, "..", "database.db")

f"""
# RSS Subscriber & Summarizer

- [OpenAPI Documents]({urllib.parse.urljoin(API_ROOT_PATH, 'docs')})
- [ReDoc Documents]({urllib.parse.urljoin(API_ROOT_PATH, 'redoc')})
- [Admin (Scheduler)]({urllib.parse.urljoin(API_ROOT_PATH, 'admin')})
- [RSSHub Document](https://docs.rsshub.app/guide/)
"""

# https://stackoverflow.com/questions/61814887/how-to-convert-a-list-of-pydantic-basemodels-to-pandas-dataframe


@st.cache_data
def get_configure() -> dict[str, dict[str, str] | None]:
    return requests.get(f"{urllib.parse.urljoin(API_REQUEST_ROOT, 'configure')}").json()


st.subheader("Configured Server")
st.json(get_configure())


# https://stackoverflow.com/questions/63881885/fastapi-get-request-with-pydantic-list-field/70845425#70845425
@st.cache_data
def get_feed_sources() -> dict:
    return requests.get(
        f"{urllib.parse.urljoin(API_REQUEST_ROOT, 'feed_sources')}"
    ).json()


import sqlite3
import pandas as pd


# TODO: maybe support all other database => use SQLModel/SQLAlchemy way..?
@st.cache_data
def get_feed_sources_with_entry_count() -> pd.DataFrame:
    conn = sqlite3.connect(DATABASE_PATH)
    query = """
    SELECT 
        RSSHubFeedEntry.rss_source, 
        COUNT(*) AS count, 
        RSSHubFeedSource.* 
    FROM 
        RSSHubFeedEntry 
    INNER JOIN 
        RSSHubFeedSource 
    ON 
        RSSHubFeedEntry.rss_source = RSSHubFeedSource.name 
    GROUP BY 
        RSSHubFeedEntry.rss_source;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.subheader("All RSS Feed Sources")
feed_sources = get_feed_sources()
st.dataframe(pd.DataFrame(feed_sources))


st.subheader("All RSS Feed Sources with Counts")
st.dataframe(get_feed_sources_with_entry_count())
