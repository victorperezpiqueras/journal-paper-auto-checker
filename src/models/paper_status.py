from dataclasses import dataclass


@dataclass
class PaperStatus:
    title: str
    step: str
    status: str
    status_date: str
    link: str
