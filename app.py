from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin
from contextlib import asynccontextmanager
from RSubscribeSummarizer.data.fetcher import RSSFeedFetcher
from RSubscribeSummarizer.data.parser import RSSHubFeedParser
from RSubscribeSummarizer.data.model import RSSHubFeedEntry, RSSHubFeedSource
from RSubscribeSummarizer.utils.logger import get_logger
from sqlmodel import create_engine, SQLModel, Session, select


logger = get_logger("FastAPI", log_file_path="./log/FastAPI.log")

rss_urls: list[str] = ["https://rsshub.app/wallstreetcn/live/global/2"]

# Create the database engine
# TODO: Make this option
sqlite_file_name = "database.db"
# TODO: Able to use other database
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)
parser = RSSHubFeedParser()
fetcher = RSSFeedFetcher(
    parser, engine, override=False, log_file_path="./log/RSSFeedFetcher.log"
)

# Create the database table
SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
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

# # Custom timed task scheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.jobstores.redis import RedisJobStore
# # Use `RedisJobStore` to create a job store
# scheduler = AsyncIOScheduler(jobstores={'default':RedisJobStore(db=2,host="127.0.0.1",port=6379,password="test")})
# scheduler = SchedulerAdmin.bind(site, scheduler=scheduler)

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
    # TODO: make this more elegant
    logger.info("Trigger fetch all")
    # TODO: Make interval a GET argument
    fetcher.fetch_all(rss_urls, interval=3)


# Start the scheduled task scheduler
scheduler.start()


@app.get("/feed_sources")
def get_feed_sources() -> list[RSSHubFeedSource]:
    logger.info("Get feed sources")
    with Session(engine) as session:
        sources = session.exec(select(RSSHubFeedSource)).all()
    return sources


if __name__ == "__main__":
    import uvicorn

    # TypeError: run() got an unexpected keyword argument 'debug'
    # uvicorn.run(app, debug=True)
    uvicorn.run(app)
