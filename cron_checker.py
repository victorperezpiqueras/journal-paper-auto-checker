import json
import logging
import os
import boto3

from status_scraper import scrap
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event=None, context=None):
    logger.info(str(os.getenv("SENDER_EMAIL")))
    journal_url = os.getenv("JOURNAL_URL")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    try:
        data = scrap(journal_url, username, password)
    except Exception as e:
        logger.error(e)
        return

    # create ses client
    ses = boto3.client("ses")

    # send message to email list
    # remove trailing ':

    emails = json.loads(os.getenv("EMAIL_ADDRESSES").strip("'"))
    result = ses.send_email(
        Source=str(os.getenv("SENDER_EMAIL")),
        Destination={"BccAddresses": emails},
        Message={
            "Subject": {"Data": f"[{data.title}] Status: {data.status}"},
            "Body": {
                "Text": {
                    "Data": f"Your paper titled: '{data.title}' \nIs in step: '{data.step}' \nWith status: '{data.status}' \nSince: {data.status_date}."
                }
            },
        },
    )
    print(result)
    return


if __name__ == "__main__":
    handler()
