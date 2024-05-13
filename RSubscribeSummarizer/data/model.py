from typing import Self
from sqlmodel import Field, SQLModel
from datetime import datetime
from feedparser.util import FeedParserDict
from .clean import markdownify
import json
from datetime import datetime
from time import mktime


class RSSHubFeedEntry(SQLModel, table=True):
    """
    TODO: whether to parse the link and preserve HTML

    TODO: if content is empty => get the HTML
    TODO: if content is pdf link => download and parse

    Extract keywords
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
                # *** ValueError: invalid literal for int() with base 10: 'undefined'
                content=markdownify(entry.summary, strip=["a", "img"]).strip(),
                raw_json=json.dumps(entry, ensure_ascii=False),
                # rss_source=rss_source,
            )
        except Exception as e:
            print(e)
            print(entry)
            # import ipdb
            # ipdb.set_trace()
            # BUG: no author
            # {'title': '国债期货收盘，30年期主力合约跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。', 'title_detail': {'type': 'text/plain', 'language': None, 'base': '', 'value': '国债期货收盘，30年期主力合约跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。'}, 'summary': '<p>国债期货收盘，30年期主力合约跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。</p>', 'summary_detail': {'type': 'text/html', 'language': None, 'base': '', 'value': '<p>国债期货收盘，30年期主力合约 跌0.29%，10年期主力合约涨0.01%，5年期主力合约跌0.00%，2年期主力合约跌0.00%。</p>'}, 'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://wallstreetcn.com/livenews/2705131'}], 'link': 'https://wallstreetcn.com/livenews/2705131', 'id': 'https://wallstreetcn.com/livenews/2705131', 'guidislink': False, 'published': 'Fri, 10 May 2024 07:15:00 GMT', 'published_parsed': time.struct_time(tm_year=2024, tm_mon=5, tm_mday=10, tm_hour=7, tm_min=15, tm_sec=0, tm_wday=4, tm_yday=131, tm_isdst=0)}
            # TODO: add logger
            # BUG: invalid literal for int() with base 10: 'undefined'
            # {'title': 'Euro-Zone Economy Picking Up Pace as Germany Heals, Survey Shows', 'title_detail': {'type': 'text/plain', 'language': None, 'base': '', 'value': 'Euro-Zone Economy Picking Up Pace as Germany Heals, Survey Shows'}, 'summary': 'The euro-are economy will expand more quickly than previously thought this year as the bloc’s biggest member exits more than a year of near-stagnation, a Bloomberg poll of analysts showed.<figure><img alt="Economists Are More Upbeat on Euro-Area Growth This Year |" src="https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iUePgj7QeYTw/v0/-1x-1.png" style="display: block; margin-left: auto; margin-right: auto;" />  </figure><div></div><p>The euro-are economy will expand more quickly than previously thought this year as the bloc’s biggest member exits more than a year of near-stagnation, a Bloomberg poll of analysts showed.</p><p>Output in the 20-nation currency union will rise by 0.7% in 2024 — more than the 0.5% advance that was forecast in the last monthly survey. Gross domestic product in Germany is now seen increasing by 0.2% compared with 0.1% before.</p><figure>  Economists Are More Upbeat on Euro-Area Growth This Year   <noscript><img alt="" src="https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iUePgj7QeYTw/v0/pidjEfPlU1QWZop3vfGKsrX.ke8XuWirGYh1PKgEw44kE/-1x-1.png" style="display: block; margin-left: auto; margin-right: auto;" /></noscript>  <figcaption><div class="source">Source: Bloomberg survey of economists conducted May 3-8</div>  <p>Note: Prior forecast conducted April 5-12</p>  </figcaption>  </figure><p>The results, which also include upgrades to the outlooks in France, Italy and Spain, capture the improving mood in the region. First-quarter GDP readings <a href="https://www.bloomberg.com/news/articles/2024-04-30/europe-gdp-latest-france-grows-in-hope-region-out-of-recession" target="_blank">surprised to the upside</a>, inflation is receding toward 2% and the European Central Bank is gearing up to start lowering interest rates.</p><p>Respondents in the survey predict three quarter-point reductions this year in the deposit rate, which currently stands at 4%. That’s about in line with the view of money-market investors.</p><figure>  Forecasts 2024 GDP Also Raised for Major Euro-Area Economies   <noscript><img alt="" src="https://assets.bwbx.io/images/users/iqjWHBFdfxIU/i1g7fOVEtG60/v0/pidjEfPlU1QWZop3vfGKsrX.ke8XuWirGYh1PKgEw44kE/-1x-1.png" style="display: block; margin-left: auto; margin-right: auto;" /></noscript>  <figcaption><div class="source">Source: Source: Bloomberg survey of economists conducted May 3-8\n\n</div>  <p>Note: Prior forecast conducted April 5-12</p>  </figcaption>  </figure><p>ECB President Christine Lagarde said last month that the euro zone economy is “recovering and we are clearly seeing signs of <a href="https://www.bloomberg.com/news/articles/2024-04-17/lagarde-says-euro-zone-economy-clearly-showing-signs-of-recovery" target="_blank">recovery</a>.”</p><table><tbody><tr><th colspan="1">Read More on the Euro-Zone Economy: </th></tr><tr><td colspan="undefined"><p><a href="https://www.bloomberg.com/news/articles/2024-05-06/euro-zone-economy-needs-consumers-to-get-out-and-spend" target="_blank">Euro Zone at Turning Point Needs Consumers to Get Out, Spend </a></p><p><a href="https://www.bloomberg.com/news/articles/2024-04-30/europe-gdp-latest-france-grows-in-hope-region-out-of-recession" target="_blank">Euro Zone Speeds Out of Recession But Inflation Is Sticky</a></p><p><a href="https://www.bloomberg.com/news/articles/2024-05-02/euro-zone-pay-growth-stays-firm-in-first-quarter-citigroup-says" target="_blank">Euro-Zone Pay Growth Stays Firm in First Quarter, Citigroup Says</a></p></td></tr></tbody></table><div></div>', 'summary_detail': {'type': 'text/html', 'language': None, 'base': '', 'value': 'The euro-are economy will expand more quickly than previously thought this year as the bloc’s biggest member exits more than a year of near-stagnation, a Bloomberg poll of analysts showed.<figure><img alt="Economists Are More Upbeat on Euro-Area Growth This Year |" src="https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iUePgj7QeYTw/v0/-1x-1.png" style="display: block; margin-left: auto; margin-right: auto;" />  </figure><div></div><p>The euro-are economy will expand more quickly than previously thought this year as the bloc’s biggest member exits more than a year of near-stagnation, a Bloomberg poll of analysts showed.</p><p>Output in the 20-nation currency union will rise by 0.7% in 2024 — more than the 0.5% advance that was forecast in the last monthly survey. Gross domestic product in Germany is now seen increasing by 0.2% compared with 0.1% before.</p><figure>  Economists Are More Upbeat on Euro-Area Growth This Year   <noscript><img alt="" src="https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iUePgj7QeYTw/v0/pidjEfPlU1QWZop3vfGKsrX.ke8XuWirGYh1PKgEw44kE/-1x-1.png" style="display: block; margin-left: auto; margin-right: auto;" /></noscript>  <figcaption><div class="source">Source: Bloomberg survey of economists conducted May 3-8</div>  <p>Note: Prior forecast conducted April 5-12</p>  </figcaption>  </figure><p>The results, which also include upgrades to the outlooks in France, Italy and Spain, capture the improving mood in the region. First-quarter GDP readings <a href="https://www.bloomberg.com/news/articles/2024-04-30/europe-gdp-latest-france-grows-in-hope-region-out-of-recession" target="_blank">surprised to the upside</a>, inflation is receding toward 2% and the European Central Bank is gearing up to start lowering interest rates.</p><p>Respondents in the survey predict three quarter-point reductions this year in the deposit rate, which currently stands at 4%. That’s about in line with the view of money-market investors.</p><figure>  Forecasts 2024 GDP Also Raised for Major Euro-Area Economies   <noscript><img alt="" src="https://assets.bwbx.io/images/users/iqjWHBFdfxIU/i1g7fOVEtG60/v0/pidjEfPlU1QWZop3vfGKsrX.ke8XuWirGYh1PKgEw44kE/-1x-1.png" style="display: block; margin-left: auto; margin-right: auto;" /></noscript>  <figcaption><div class="source">Source: Source: Bloomberg survey of economists conducted May 3-8\n\n</div>  <p>Note: Prior forecast conducted April 5-12</p>  </figcaption>  </figure><p>ECB President Christine Lagarde said last month that the euro zone economy is “recovering and we are clearly seeing signs of <a href="https://www.bloomberg.com/news/articles/2024-04-17/lagarde-says-euro-zone-economy-clearly-showing-signs-of-recovery" target="_blank">recovery</a>.”</p><table><tbody><tr><th colspan="1">Read More on the Euro-Zone Economy: </th></tr><tr><td colspan="undefined"><p><a href="https://www.bloomberg.com/news/articles/2024-05-06/euro-zone-economy-needs-consumers-to-get-out-and-spend" target="_blank">Euro Zone at Turning Point Needs Consumers to Get Out, Spend </a></p><p><a href="https://www.bloomberg.com/news/articles/2024-04-30/europe-gdp-latest-france-grows-in-hope-region-out-of-recession" target="_blank">Euro Zone Speeds Out of Recession But Inflation Is Sticky</a></p><p><a href="https://www.bloomberg.com/news/articles/2024-05-02/euro-zone-pay-growth-stays-firm-in-first-quarter-citigroup-says" target="_blank">Euro-Zone Pay Growth Stays Firm in First Quarter, Citigroup Says</a></p></td></tr></tbody></table><div></div>'}, 'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://www.bloomberg.com/news/articles/2024-05-13/euro-zone-economy-picking-up-pace-as-germany-heals-survey-shows'}], 'link': 'https://www.bloomberg.com/news/articles/2024-05-13/euro-zone-economy-picking-up-pace-as-germany-heals-survey-shows', 'id': 'bloomberg:SD9J37T0G1KW00', 'guidislink': False, 'published': 'Mon, 13 May 2024 04:00:00 GMT', 'published_parsed': time.struct_time(tm_year=2024, tm_mon=5, tm_mday=13, tm_hour=4, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=134, tm_isdst=0), 'authors': [{'name': 'Andrew Langley, Harumi Ichikura'}], 'author': 'Andrew Langley, Harumi Ichikura', 'author_detail': {'name': 'Andrew Langley, Harumi Ichikura'}, 'tags': [{'term': 'Germany', 'scheme': None, 'label': None}, {'term': 'SURVEY SAS', 'scheme': None, 'label': None}, {'term': 'GDP', 'scheme': None, 'label': None}, {'term': 'Currency', 'scheme': None, 'label': None}, {'term': 'European Central Bank', 'scheme': None, 'label': None}, {'term': 'France', 'scheme': None, 'label': None}, {'term': 'Italy', 'scheme': None, 'label': None}, {'term': 'Spain', 'scheme': None, 'label': None}, {'term': 'Euro Spot', 'scheme': None, 'label': None}, {'term': 'Interest Rates', 'scheme': None, 'label': None}], 'media_content': [{'url': 'https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iUePgj7QeYTw/v0/-1x-1.png'}], 'media_thumbnails': {'url': 'https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iUePgj7QeYTw/v0/-1x-1.png'}}
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
