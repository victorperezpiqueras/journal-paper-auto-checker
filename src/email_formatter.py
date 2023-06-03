from paper_status import PaperStatus


class EmailFormatter:
    def __init__(self, status: PaperStatus):
        self.status = status

    def get_subject(self) -> str:
        return f"[{self.status.status}]: {self.status.title}"

    def get_body(self) -> str:
        return (
            f"Your paper titled: <b>'{self.status.title}'</b>\n"
            f"Is in step: <b>'{self.status.step}'</b>\n"
            f"Status: <b>'{self.status.status}'</b>\n"
            f"Status Date: <b>{self.status.status_date}</b>"
        )
