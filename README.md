# RSubscribeSummarizer

An RSS subscriber and information summarizer.

## Getting Started

```bash
pip install -r requirements.txt
# Simple Test
python main.py
# API Server
fastapi dev ./app.py
```

Using Docker

```bash
docker compose up --build
```

Migration

```bash
alembic revision --autogenerate -m "migration commit"
python3.11 -m alembic revision --autogenerate -m "migration commit"
docker-compose exec api alembic revision --autogenerate -m "migration commit"
```

## Todo

- [ ] Compress output with [zstd](https://github.com/facebook/zstd)
- [ ] Use database
  - [X] SQLite
  - [ ] PostgreSQL with docker compose [testdrivenio/fastapi-sqlmodel-alembic: Sample FastAPI project that uses async SQLAlchemy, SQLModel, Postgres, Alembic, and Docker.](https://github.com/testdrivenio/fastapi-sqlmodel-alembic/tree/main)
- [ ] YAML Configure file to config
  1. source
  2. frequency
  3. additional processing modules (e.g. NER, tags)
- [ ] Search/Retrieval on parsed data
  - Elastic Search [elastic/elasticsearch: Free and Open, Distributed, RESTful Search Engine](https://github.com/elastic/elasticsearch)
  - VectorDB
- [ ] Send feed or summarized feed to downstream subscription (e.g. Discord webhook)
- [ ] Know how to do the database migration when data model schema change => Alembic

## Resources

RSS Source

- [DIYgod/RSSHub: 🧡 Everything is RSSible](https://github.com/DIYgod/RSSHub) [Welcome to RSSHub!](https://rsshub.app/)
  - [Getting Started | RSSHub](https://docs.rsshub.app/guide/)
  - [RSS Feed Fundamentals | RSSHub](https://docs.rsshub.app/joinus/advanced/advanced-feed) - schema

Parser

- [kurtmckee/feedparser: Parse feeds in Python](https://github.com/kurtmckee/feedparser)
- [Reader API](https://jina.ai/reader)

API

- [FastAPI](https://fastapi.tiangolo.com/)
  - [tiangolo/fastapi: FastAPI framework, high performance, easy to learn, fast to code, ready for production](https://github.com/tiangolo/fastapi)
  - Web Page
    - [FastAPI — Render Template & Redirection | by Sarumathy P | featurepreneur | Medium](https://medium.com/featurepreneur/fastapi-render-template-redirection-c98a26ae1e2a)
- ASPScheduler
  - Wrapper
    - [amisadmin/fastapi-scheduler: FastAPI-Scheduler is a simple scheduled task management FastAPI extension based on APScheduler.](https://github.com/amisadmin/fastapi-scheduler)
    - [amisadmin/fastapi-amis-admin: FastAPI-Amis-Admin is a high-performance, efficient and easily extensible FastAPI admin framework. Inspired by django-admin, and has as many powerful functions as django-admin.](https://github.com/amisadmin/fastapi-amis-admin)
  - Native
    - [Implementing Background Job Scheduling in FastAPI with APScheduler | by Rajan Sahu | Mar, 2024 | Medium](https://rajansahu713.medium.com/implementing-background-job-scheduling-in-fastapi-with-apscheduler-6f5fdabf3186)
