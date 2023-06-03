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
    journal_configs_query_response = journal_dynamodb_table.query(
        KeyConditionExpression="pK = :pK",
        ExpressionAttributeValues={":pK": "CONFIG"},
    )
    # parse to list:
    journal_configs = journal_configs_query_response["Items"]

    # for each journal config, scrap and send email:
    for journal_config in journal_configs:
        journal_type = journal_config["payload"]["journal"]
        username = journal_config["payload"]["username"]
        password = journal_config["payload"]["password"]
        destination_addresses = journal_config["payload"]["destination_addresses"]
        journal = journal_factory(journal_type)
        try:
            # paper_status = scrap(journal_url, username, password)
            logger.info(f"Scraping {journal_type}")
            paper_status = journal.scrap(username, password)
        except Exception as e:
            logger.error(e)
            continue

        # store paper status in dynamodb
        journal_dynamodb_table.put_item(
            Item={
                "pK": f"STATUS#{journal_type}",
                "timestamp": int(time.time() * 1000),
                "payload": paper_status.__dict__,
            }
        )

        # build email content
        email_formatter = EmailFormatter(paper_status)
        # destination_addresses = json.loads(os.getenv("EMAIL_ADDRESSES").strip("'"))
        raw_message = email_formatter.get_raw_email_message(
            os.getenv("SENDER_EMAIL"), destination_addresses, bcc=True
        )

        ses = boto3.client("ses")
        try:
            ses.send_raw_email(
                Source=str(os.getenv("SENDER_EMAIL")),
                Destinations=destination_addresses,
                RawMessage={"Data": raw_message},
            )
            logging.info(f"Email sent to {destination_addresses}")
        except Exception as e:
            logging.error(e)
            continue
    return
