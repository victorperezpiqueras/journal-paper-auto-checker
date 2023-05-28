import json
import logging
import os
import boto3

from src.status_scraper import scrap


def handler(event=None, context=None):
    journal_url = os.getenv("JOURNAL_URL")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    data = scrap(journal_url, username, password)

    # create ses client
    ses = boto3.client("ses")

    # send message to email list
    emails = json.loads(os.getenv("EMAIL_ADDRESSES"))
    result = ses.send_email(
        Source=os.getenv("SENDER_EMAIL"),
        Destination={"BccAddresses": emails},
        Message={
            "Subject": {"Data": f"[{data['title']}] Status: {data['status']}"},
            "Body": {
                "Text": {
                    "Data": f"Your paper titled: '{data['title']}' \nIs in step: '{data['step']}' \nWith status: '{data['status']}' \nSince: {data['status_date']}."
                }
            },
        },
    )
    logging.info(result)
    return


if __name__ == "__main__":
    handler()
