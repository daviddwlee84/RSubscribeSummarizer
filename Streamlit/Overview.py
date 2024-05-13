import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, ".."))
from RSubscribeSummarizer.data.model import RSSHubFeedEntry, RSSHubFeedSource  # noqa


"""
RSS Subscriber & Summarizer</h1>

- [OpenAPI Documents](/api/docs)
- [ReDoc Documents](/api/redoc)
- [Admin (Scheduler)](/api/admin)
"""
