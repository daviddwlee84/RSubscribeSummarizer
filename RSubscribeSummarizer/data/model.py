from typing import Self
from sqlmodel import Field, SQLModel
from datetime import datetime
from feedparser.util import FeedParserDict
from markdownify import markdownify
import json
from datetime import datetime
from time import mktime


class RSSHubFeedEntry(SQLModel, table=True):
    """
    TODO: whether to parse the link and preserve HTML
    """

    # https://github.com/tiangolo/sqlmodel/issues/159
    __tablename__: str = "RSSHubFeedEntry"

    # NOTE: this will be an automatically increase id
    # https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
    id: int | None = Field(default=None, primary_key=True)
    original_id: str
    title: str
    author: str | None
    link: str
    content: str
    time: datetime
    raw_json: str
    # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/define-relationships-attributes/
    rss_source: str | None = Field(default=None, foreign_key="RSSHubFeedSource.name")

    @classmethod
    def from_feedparser_entry(
        cls,
        entry: FeedParserDict,
        rss_source: str | None = None,
        table_name: str | None = None,
    ) -> Self:
        try:
            entry_object = cls(
                original_id=entry.id,
                title=entry.title,
                author=entry.get("author"),
                time=datetime.fromtimestamp(mktime(entry.published_parsed)),
                link=entry.link,
                content=markdownify(entry.summary, strip=["a", "img"]).strip(),
                raw_json=json.dumps(entry, ensure_ascii=False),
            )
        except Exception as e:
            print(e)
            print(entry)
            # {'title': '国债期货收盘，30年期主力合约跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。', 'title_detail': {'type': 'text/plain', 'language': None, 'base': '', 'value': '国债期货收盘，30年期主力合约跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。'}, 'summary': '<p>国债期货收盘，30年期主力合约跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。</p>', 'summary_detail': {'type': 'text/html', 'language': None, 'base': '', 'value': '<p>国债期货收盘，30年期主力合约 跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。</p>'}, 'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://wallstreetcn.com/livenews/2705131'}], 'link': 'https://wallstreetcn.com/livenews/2705131', 'id': 'https://wallstreetcn.com/livenews/2705131', 'guidislink': False, 'published': 'Fri, 10 May 2024 07:15:00 GMT', 'published_parsed': time.struct_time(tm_year=2024, tm_mon=5, tm_mday=10, tm_hour=7, tm_min=15, tm_sec=0, tm_wday=4, tm_yday=131, tm_isdst=0)}
            # TODO: add logger
        if rss_source is not None:
            entry_object.rss_source = rss_source
        if table_name is not None:
            entry_object.__tablename__ = table_name
        return entry_object

    @property
    def key_to_dedup(self) -> str:
        # NOTE: this is feedparser's id
        return "original_id"


class RSSHubFeedSource(SQLModel, table=True):
    """
    TODO: maybe store last update time to determine when to refresh from this source
    """

    __tablename__: str = "RSSHubFeedSource"

    # NOTE: this will be an automatically increase id
    # https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
    name: str = Field(primary_key=True)
    url: str
    title: str
    link: str
    updated_time: datetime
    raw_json: str

    @classmethod
    def from_feedparser_feed(
        cls,
        name: str,
        url: str,
        feed: FeedParserDict,
        table_name: str | None = None,
    ) -> Self:
        feed_object = cls(
            name=name,
            url=url,
            title=feed.title,
            link=feed.link,
            updated_time=datetime.fromtimestamp(mktime(feed.updated_parsed)),
            raw_json=json.dumps(feed, ensure_ascii=False),
        )
        if table_name is not None:
            feed_object.__tablename__ = table_name
        return feed_object

    @property
    def key_to_dedup(self) -> str:
        # NOTE: this is feedparser's id
        return "url"
