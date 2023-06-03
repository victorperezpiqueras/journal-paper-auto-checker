from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import logging
import os
import boto3
from email_formatter import EmailFormatter
from status_scraper import scrap
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event=None, context=None):
    journal_url = os.getenv("JOURNAL_URL")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    try:
        paper_status = scrap(journal_url, username, password)
    except Exception as e:
        logger.error(e)
        return

    # build email content
    email_formatter = EmailFormatter(paper_status)
    destination_addresses = json.loads(os.getenv("EMAIL_ADDRESSES").strip("'"))
    raw_message = email_formatter.get_raw_email_message(
        os.getenv("SENDER_EMAIL"), destination_addresses, bcc=True
    )

    ses = boto3.client("ses")
    result = ses.send_raw_email(
        Source=str(os.getenv("SENDER_EMAIL")),
        Destinations=destination_addresses,
        RawMessage={"Data": raw_message},
    )
    logging.info(f"Email sent to {destination_addresses}")
    return
