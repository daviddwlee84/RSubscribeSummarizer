from sqlmodel import create_engine, SQLModel
from sqlalchemy import Engine
from RSubscribeSummarizer.data.parser import RSSHubFeedParser
from RSubscribeSummarizer.data.fetcher import RSSFeedFetcher
from RSubscribeSummarizer.utils.logger import get_logger


def _single_fetch_test(engine: Engine):
    fetcher = RSSFeedFetcher(
        ["https://rsshub.app/wallstreetcn/live/global/2"],
        RSSHubFeedParser(),
        engine,
        override=False,
    )

    fetcher.fetch("https://rsshub.app/wallstreetcn/live/global/2")

    from sqlmodel import Session, select
    from RSubscribeSummarizer.data.model import RSSHubFeedEntry, RSSHubFeedSource

    with Session(engine) as session:
        for source in session.exec(select(RSSHubFeedSource)).all():
            print(source)
        for entry in session.exec(select(RSSHubFeedEntry)).all():
            print(entry)
        import ipdb

        ipdb.set_trace()


if __name__ == "__main__":
    logger = get_logger("Main")

    # Create the database engine
    # TODO: Make this option
    sqlite_file_name = "database.db"
    # TODO: Able to use other database
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    # engine = create_engine(sqlite_url, echo=True)
    engine = create_engine(sqlite_url, echo=False)

    # Create the database table
    SQLModel.metadata.create_all(engine)

    _single_fetch_test(engine)
