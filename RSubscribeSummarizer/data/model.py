from typing import Optional, Self
from sqlmodel import Field, SQLModel
from datetime import datetime
from feedparser.util import FeedParserDict
from markdownify import markdownify
import json
from datetime import datetime
from time import mktime


class RSSHubFeedEntry(SQLModel, table=True):

    __tablename__: str = "RSSHubFeedEntry"

    # NOTE: this will be an automatically increase id
    # https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
    id: Optional[int] = Field(default=None, primary_key=True)
    original_id: str
    title: str
    author: str
    link: str
    content: str
    time: datetime
    raw_json: str
    rss_source: Optional[str] = None

    @classmethod
    def from_feedparser_entry(
        cls,
        entry: FeedParserDict,
        rss_source: Optional[str] = None,
        table_name: Optional[str] = None,
    ) -> Self:
        entry_object = cls(
            original_id=entry.id,
            title=entry.title,
            author=entry.author,
            time=datetime.fromtimestamp(mktime(entry.published_parsed)),
            link=entry.link,
            content=markdownify(entry.summary, strip=["a", "img"]).strip(),
            raw_json=json.dumps(entry, ensure_ascii=False),
        )
        if rss_source is not None:
            entry_object.rss_source = rss_source
        if table_name is not None:
            entry_object.__tablename__ = table_name
        return entry_object


class RSSHubFeedSource(SQLModel, table=True):
    """
    TODO: maybe store last update time to determine when to refresh from this source
    """

    __tablename__: str = "RSSHubFeedSource"

    # NOTE: this will be an automatically increase id
    # https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
    url: str = Field(primary_key=True)
    title: str
    link: str
    updated_time: datetime
    raw_json: str

    @classmethod
    def from_feedparser_feed(
        cls,
        url: str,
        feed: FeedParserDict,
        table_name: Optional[str] = None,
    ) -> Self:
        feed_object = cls(
            url=url,
            title=feed.title,
            link=feed.link,
            updated_time=datetime.fromtimestamp(mktime(feed.updated_parsed)),
            raw_json=json.dumps(feed, ensure_ascii=False),
        )
        if table_name is not None:
            feed_object.__tablename__ = table_name
        return feed_object
