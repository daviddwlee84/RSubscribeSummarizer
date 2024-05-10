# RSubscribeSummarizer

An RSS subscriber and information summarizer.

## Todo

- [ ] Compress output with [zstd](https://github.com/facebook/zstd)
- [ ] Use database
  - [X] SQLite
  - [ ] PostgreSQL with docker compose
- [ ] YAML Configure file to config
  1. source
  2. frequency
  3. additional processing modules (e.g. NER, tags)
- [ ] Search/Retrieval on parsed data
  - Elastic Search [elastic/elasticsearch: Free and Open, Distributed, RESTful Search Engine](https://github.com/elastic/elasticsearch)
  - VectorDB
- [ ] Send feed or summarized feed to downstream subscription (e.g. Discord webhook)

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
- [amisadmin/fastapi-scheduler: FastAPI-Scheduler is a simple scheduled task management FastAPI extension based on APScheduler.](https://github.com/amisadmin/fastapi-scheduler)
- [amisadmin/fastapi-amis-admin: FastAPI-Amis-Admin is a high-performance, efficient and easily extensible FastAPI admin framework. Inspired by django-admin, and has as many powerful functions as django-admin.](https://github.com/amisadmin/fastapi-amis-admin)
