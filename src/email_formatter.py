from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from paper_status import PaperStatus


class EmailFormatter:
    def __init__(self, status: PaperStatus):
        self.status = status

    def _get_subject(self) -> str:
        return f"[{self.status.status}]: {self.status.title}"

    def _get_body(self) -> str:
        return (
            f"Your paper titled: <b>{self.status.title}</b><br>"
            f"Is in step: <b>{self.status.step}</b><br>"
            f"Status: <b>{self.status.status}</b><br>"
            f"Status Date: <b>{self.status.status_date}</b><br>"
            f"Link to paper: <a href='{self.status.link}'>{self.status.link}</a><br>"
        )

    def get_raw_email_message(
        self, from_address: str, to_addresses: list[str], bcc: bool = True
    ) -> str:
        msg = MIMEMultipart()
        msg["Subject"] = self._get_subject()
        msg["From"] = from_address
        if bcc:
            msg["Bcc"] = ", ".join(to_addresses)
        else:
            msg["To"] = ", ".join(to_addresses)
        email_body = self._get_body()
        msg.attach(MIMEText(email_body, "html"))
        return msg.as_string()
