from typing import Optional
import feedparser
from feedparser.util import FeedParserDict
from .model import RSSHubFeedEntry, RSSHubFeedSource
import requests


class BaseRSSFeedParser:
    @staticmethod
    def fetch(url: str) -> Optional[FeedParserDict]:
        raise NotImplementedError()

    @staticmethod
    def parse(
        feed: FeedParserDict, url: str
    ) -> tuple[RSSHubFeedSource, list[RSSHubFeedEntry]]:
        """
        The `url` is treated as a metadata, not involves in the RSS Parse progress
        """
        raise NotImplementedError()

    def __call__(
        self, source_name: str, url: str
    ) -> tuple[RSSHubFeedSource, list[RSSHubFeedEntry]]:
        feed = self.fetch(url)
        source, entries = self.parse(feed, source_name, url)
        return source, entries


class RSSHubFeedParser(BaseRSSFeedParser):
    @staticmethod
    def fetch(url: str) -> Optional[FeedParserDict]:
        """
        TODO: add retry mechanism
        https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
        """
        response = requests.get(url)
        if response.status_code != 200:
            # TODO: warning, retry, etc.
            return None
        return feedparser.parse(response.content.decode("utf-8"))

    @staticmethod
    def parse(
        feed: FeedParserDict, source_name: str, url: str
    ) -> tuple[RSSHubFeedSource, list[RSSHubFeedEntry]]:
        feed_source = RSSHubFeedSource.from_feedparser_feed(source_name, url, feed.feed)
        feed_entries = [
            RSSHubFeedEntry.from_feedparser_entry(entry, rss_source=feed_source.name)
            for entry in feed.entries
        ]
        return feed_source, feed_entries
