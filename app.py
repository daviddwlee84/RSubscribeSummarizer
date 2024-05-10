from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin
from contextlib import asynccontextmanager
from RSubscribeSummarizer.data.fetcher import RSSFeedFetcher
from RSubscribeSummarizer.data.parser import RSSHubFeedParser
from RSubscribeSummarizer.data.model import RSSHubFeedEntry, RSSHubFeedSource
from RSubscribeSummarizer.utils.logger import get_logger
from sqlmodel import create_engine, SQLModel, Session, select, desc, asc
from fastapi.responses import HTMLResponse
import yaml

CONFIG_FILE = "config.yaml"

logger = get_logger("FastAPI", log_file_path="./log/FastAPI.log")

rss_urls: dict[str, str] = {
    "wallstreetcn_live_global_important": "https://rsshub.app/wallstreetcn/live/global/2"
}

# Create the database engine
# TODO: Make this option
sqlite_file_name = "database.db"
# TODO: Able to use other database
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)
# Create the database table
SQLModel.metadata.create_all(engine)  # , tables=[RSSHubFeedEntry, RSSHubFeedSource])
parser = RSSHubFeedParser()
fetcher = RSSFeedFetcher(
    parser, engine, override=False, log_file_path="./log/RSSFeedFetcher.log"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configure rss_urls
    configure()
    yield
    # TODO: scheduler.shutdown()


# Create `FastAPI` application
app = FastAPI(lifespan=lifespan)

# Create `AdminSite` instance
site = AdminSite(
    settings=Settings(
        database_url_async="sqlite+aiosqlite:///amisadmin.db",
        language="en_US",
        logger=logger,
    )
)

# Create an instance of the scheduled task scheduler `SchedulerAdmin`
scheduler = SchedulerAdmin.bind(site)

# Mount the background management system
site.mount_app(app)


# Add scheduled tasks, refer to the official documentation: https://apscheduler.readthedocs.io/en/master/
# use when you want to run the job at fixed intervals of time
@app.get("/fetch_all")
@scheduler.scheduled_job("interval", name="Fetch All RSS URLs", seconds=3600)
def fetch_all_rss():
    """
    Regular fetch from all given RSS and store into database
    """
    global rss_urls
    # TODO: make this more elegant
    logger.info("Trigger fetch all")
    # TODO: Make interval a GET argument
    fetcher.fetch_all(rss_urls, interval=3)


# Start the scheduled task scheduler
scheduler.start()

scheduler.get_jobs()


# https://github.com/tiangolo/full-stack-fastapi-couchbase/issues/10
# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#exclude-from-openapi
@app.get("/", include_in_schema=False)
def home() -> str:
    return HTMLResponse(
        """
    <h1>RSS Subscriber & Summarizer</h1>
    <ul>
    <li><a href="/docs">OpenAPI Documents</a></li>
    <li><a href="/redoc">ReDoc Documents</a></li>
    <li><a href="/admin">Admin (Scheduler)</a></li>
    </ul>
    """
    )


@app.get("/configure")
def configure() -> dict[str, dict[str, str] | None]:
    """
    TODO: POST to update config, GET to view config (or render a config UI) => Maybe somehow combine into AdminSite
    """
    # Update global config
    global rss_urls

    logger.info(f"Load config from {CONFIG_FILE} and update rss_urls")

    # Update global config
    with open(CONFIG_FILE, "r") as fp:
        config = yaml.safe_load(fp)

    # Update RSS URLs
    rss_urls = config.get(
        "rss_sources",
        {
            "wallstreetcn_live_global_important": "https://rsshub.app/wallstreetcn/live/global/2"
        },
    )

    # TODO: Update scheduler

    return config


@app.get("/feed_sources")
def get_feed_sources() -> list[RSSHubFeedSource]:
    logger.info("Get feed sources")
    with Session(engine) as session:
        sources = session.exec(select(RSSHubFeedSource)).all()
    return sources


# https://fastapi.tiangolo.com/tutorial/path-params/
# https://fastapi.tiangolo.com/tutorial/query-params/#optional-parameters
# https://fastapi.tiangolo.com/tutorial/query-params/#query-parameter-type-conversion
@app.get("/feed_entries", name="Get all entries")
@app.get("/feed_entries/{rss_source_name}", name="Get entries of a RSS source")
def get_feed_entries(
    rss_source_name: str | None = None,
    skip: int = 0,
    limit: int = 10,
    latest: bool = True,
) -> list[RSSHubFeedEntry]:
    """
    Retrieve entries
    """
    logger.info(f"Get feed entries by feed source {rss_source_name}")
    expression = select(RSSHubFeedEntry)
    if rss_source_name is not None:
        expression = expression.where(RSSHubFeedEntry.rss_source == rss_source_name)
    if skip > 0:
        # https://stackoverflow.com/questions/13258934/applying-limit-and-offset-to-all-queries-in-sqlalchemy
        expression = expression.offset(skip)
    if limit > 0:
        expression = expression.limit(limit)
    # https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
    if latest:
        expression = expression.order_by(desc(RSSHubFeedEntry.time))
    else:
        expression = expression.order_by(asc(RSSHubFeedEntry.time))

    with Session(engine) as session:
        entries = session.exec(expression).all()
    return entries


if __name__ == "__main__":
    import uvicorn

    # TypeError: run() got an unexpected keyword argument 'debug'
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
