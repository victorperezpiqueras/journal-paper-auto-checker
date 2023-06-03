import logging
import os
import time
import boto3
from models.email_formatter import EmailFormatter
from models.journal import journal_factory
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event=None, context=None):
    # journal_url = os.getenv("JOURNAL_URL")
    # username = os.getenv("USERNAME")
    # password = os.getenv("PASSWORD")

    # get dynamodb from os env:
    journal_dynamodb_table_name = os.getenv("JOURNAL_STATUSES_CONFIGS_DYNAMODB_TABLE")
    journal_dynamodb_table = boto3.resource("dynamodb").Table(
        journal_dynamodb_table_name
    )

    # querytable for pK equal CONFIG:
    journal_configs = journal_dynamodb_table.query(
        KeyConditionExpression="pK = :pK",
        ExpressionAttributeValues={":pK": "CONFIG"},
    )["Items"]

    # for each journal config, scrap and send email:
    for journal_config in journal_configs:
        journal_type = journal_config["payload"]["journal_type"]
        journal_url = journal_config["payload"]["journal_url"]
        username = journal_config["payload"]["username"]
        password = journal_config["payload"]["password"]
        destination_addresses = journal_config["payload"]["destination_addresses"]
        if not destination_addresses:
            logger.info(
                f"No destination addresses found for {journal_type}. Skipping it"
            )
            continue

        journal = journal_factory(journal_type, journal_url)

        try:
            logger.info(f"Scraping {journal_type}")
            paper_status = journal.scrap(username, password)
        except Exception as e:
            logger.error(e)
            continue

        current_ts = int(time.time() * 1000)
        # check status filter less than timestamp sk if exists and check if it has same data in payload:
        last_journal_status = journal_dynamodb_table.query(
            KeyConditionExpression="pK = :pK AND #timestamp < :timestamp",
            ExpressionAttributeValues={
                ":pK": f"STATUS#{journal_type}",
                ":timestamp": current_ts,
            },
            ExpressionAttributeNames={"#timestamp": "timestamp"},
            ScanIndexForward=False,
            Limit=1,
        )["Items"]

        if (
            len(last_journal_status) > 0
            and last_journal_status[0]["payload"] == paper_status.__dict__
        ):
            logger.info(f"Status for {journal_type} has not changed")
            continue

        # store paper status in dynamodb
        logger.info(f"New {journal_type} status found. Storing it in dynamodb")
        journal_dynamodb_table.put_item(
            Item={
                "pK": f"STATUS#{journal_type}",
                "timestamp": current_ts,
                "payload": paper_status.__dict__,
            }
        )

        # build email content
        email_formatter = EmailFormatter(paper_status)
        raw_message = email_formatter.get_raw_email_message(
            os.getenv("SENDER_EMAIL"), destination_addresses, bcc=True
        )

        ses = boto3.client("ses")
        try:
            logging.info(f"Sending email to {destination_addresses}")
            ses.send_raw_email(
                Source=str(os.getenv("SENDER_EMAIL")),
                Destinations=destination_addresses,
                RawMessage={"Data": raw_message},
            )
        except Exception as e:
            logging.error(e)
            continue
    return
