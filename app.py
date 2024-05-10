from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from datetime import date
from fastapi_scheduler import SchedulerAdmin
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# Create `FastAPI` application
app = FastAPI(lifespan=lifespan)

# Create `AdminSite` instance
site = AdminSite(
    settings=Settings(
        database_url_async="sqlite+aiosqlite:///amisadmin.db", language="en_US"
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

# Start the scheduled task scheduler
scheduler.start()


# Add scheduled tasks, refer to the official documentation: https://apscheduler.readthedocs.io/en/master/
# use when you want to run the job at fixed intervals of time
@scheduler.scheduled_job("interval", seconds=3600)
def fetch_all_rss():
    pass


if __name__ == "__main__":
    import uvicorn

    # TypeError: run() got an unexpected keyword argument 'debug'
    # uvicorn.run(app, debug=True)
    uvicorn.run(app)
