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

    emails = json.loads(os.getenv("EMAIL_ADDRESSES").strip("'"))
    email_formatter = EmailFormatter(paper_status)

    ses = boto3.client("ses")
    result = ses.send_email(
        Source=str(os.getenv("SENDER_EMAIL")),
        Destination={"BccAddresses": emails},
        Message={
            "Subject": {"Data": email_formatter.get_subject()},
            "Body": {
                "Text": {
                    "Data": email_formatter.get_body(),
                }
            },
        },
    )
    logging.info(f"Email sent to {emails}")
    return
