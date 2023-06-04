from dataclasses import dataclass


@dataclass
class JournalConfig:
    journal_type: str
    journal_url: str
    destination_addresses: list[str]
    username: str
    password: str
