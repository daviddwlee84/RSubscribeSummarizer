from typing import Optional
from .parser import BaseRSSFeedParser
from ..utils.logger import get_logger
from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, select
from sqlalchemy.inspection import inspect
from tqdm.autonotebook import tqdm
import time


class RSSFeedFetcher:

    def __init__(
        self,
        parser: BaseRSSFeedParser,
        engine: Engine,
        override: bool = False,
        log_file_path: Optional[str] = None,
    ) -> None:
        """
        If override then update the existing entries
        """
        self._parser = parser
        self._engine = engine
        self._logger = get_logger(self.__class__.__name__, log_file_path=log_file_path)
        self._override = override

    # @staticmethod
    # def get_primary_key_field(model: SQLModel):
    #     """Identify the primary key field of the given model."""
    #     # NOTE: use "class" to inspect the primary key
    #     return [key.name for key in inspect(model.__class__).primary_key]

    def add_or_update(self, entry: SQLModel, session: Session, override: bool) -> bool:
        """
        Add a new entry or update an existing entry based on the primary key.
        """
        # primary_keys = self.get_primary_key_field(entry)
        primary_keys = [entry.key_to_dedup]
        filters = [
            getattr(entry.__class__, key) == getattr(entry, key) for key in primary_keys
        ]

        # NOTE: use "class" so it knows "from" which table
        existing_entry = session.exec(select(entry.__class__).where(*filters)).first()

        if existing_entry:
            if not override:
                # TODO: Maybe separate the "updated" or "added"
                return False
            # TODO: not sure if this is canonical way to update existing entry
            # Update the existing entry
            for key, value in entry.model_dump().items():
                setattr(existing_entry, key, value)
            session.add(existing_entry)
            session.commit()
            self._logger.info(
                f"Updated RSS entry {entry.id} with primary key: {[getattr(entry, key) for key in primary_keys]}"
            )
        else:
            # Add the new entry
            session.add(entry)
            session.commit()
            self._logger.info(
                f"Added RSS entry {entry.id} with primary key: {[getattr(entry, key) for key in primary_keys]}"
            )
        return True

    def fetch(self, url: str) -> None:
        """
        TODO: return status
        """
        self._logger.info(f"Parsing {url}...")
        source, entries = self._parser(url)
        self._logger.info(f"Fetched {len(entries)} entries from source {source.title}.")
        count = 0
        self._logger.info(f"Updating database {self._engine}...")
        with Session(self._engine) as session:
            for item in [source] + entries:
                count += self.add_or_update(item, session, self._override)
        self._logger.info(f"{count} entries added or updated.")

    def fetch_all(self, rss_urls: list[str], interval: float = 3) -> None:
        """
        Maybe do this async..?

        TODO: return status
        """
        for url in tqdm(rss_urls, desc="Fetching RSS"):
            self.fetch(url)
            time.sleep(interval)
