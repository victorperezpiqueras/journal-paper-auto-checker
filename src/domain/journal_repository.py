from abc import ABC, abstractmethod
from typing import Optional

from domain.journal_config import JournalConfig
from domain.paper_status import PaperStatus


class JournalRepository(ABC):
    @abstractmethod
    def get_all_configs(self) -> list[JournalConfig]:
        pass

    @abstractmethod
    def get_last_journal_status(self, journal_type: str) -> Optional[PaperStatus]:
        pass

    @abstractmethod
    def save_journal_status(self, journal_type: str, paper_status: PaperStatus) -> None:
        pass


def get_journal_repository() -> JournalRepository:
    from infrastructure.dynamodb_journal_repository import DynamoDBJournalRepository

    return DynamoDBJournalRepository()
