import logging
import os
import boto3
from domain.email_formatter import EmailFormatter
from domain.journal import journal_factory
import logging

from domain.journal_repository import get_journal_repository

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event=None, context=None):
    journal_repository = get_journal_repository()
    # querytable for pK equal CONFIG:
    journal_configs = journal_repository.get_all_configs()

    # for each journal config, scrap and send email:
    for journal_config in journal_configs:
        journal_type = journal_config.journal_type
        journal_url = journal_config.journal_url
        username = journal_config.username
        password = journal_config.password
        destination_addresses = journal_config.destination_addresses
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

        last_journal_status = journal_repository.get_last_journal_status(journal_type)

        if (
            last_journal_status is not None
            and last_journal_status.__dict__ == paper_status.__dict__
        ):
            logger.info(f"Status for {journal_type} has not changed")
            continue

        logger.info(f"New {journal_type} status found. Storing it")
        journal_repository.save_journal_status(journal_type, paper_status)

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
