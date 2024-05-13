import sys
import os
import requests
import urllib.parse
import streamlit as st

curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, ".."))
from RSubscribeSummarizer.data.model import RSSHubFeedEntry, RSSHubFeedSource  # noqa

API_ROOT_PATH = "/api"
API_REQUEST_ROOT = "http://api:8000"

f"""
# RSS Subscriber & Summarizer

- [OpenAPI Documents]({urllib.parse.urljoin(API_ROOT_PATH, 'docs')})
- [ReDoc Documents]({urllib.parse.urljoin(API_ROOT_PATH, 'redoc')})
- [Admin (Scheduler)]({urllib.parse.urljoin(API_ROOT_PATH, 'admin')})
"""

# https://stackoverflow.com/questions/61814887/how-to-convert-a-list-of-pydantic-basemodels-to-pandas-dataframe


@st.cache_data
def get_configure() -> dict[str, dict[str, str] | None]:
    return requests.get(f"{urllib.parse.urljoin(API_REQUEST_ROOT, 'configure')}").json()


st.subheader("Configured Server")
st.json(get_configure())

# https://stackoverflow.com/questions/63881885/fastapi-get-request-with-pydantic-list-field/70845425#70845425
# @st.cache_data
# def get_feed_sources() -> dict[str, dict[str, str] | None]:
#     return requests.get(
#         f"{urllib.parse.urljoin(API_REQUEST_ROOT, 'feed_sources')}"
#     ).json()
#
# st.subheader("All RSS Feed Sources")
