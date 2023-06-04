import os
import time
from typing import Optional
import boto3
from domain.journal_config import JournalConfig
from domain.paper_status import PaperStatus
from domain.journal_repository import JournalRepository


class DynamoDBJournalRepository(JournalRepository):
    def __init__(self):
        journal_dynamodb_table_name = os.getenv(
            "JOURNAL_STATUSES_CONFIGS_DYNAMODB_TABLE"
        )
        self.journal_dynamodb_table = boto3.resource("dynamodb").Table(
            journal_dynamodb_table_name
        )

    def get_all_configs(self) -> list[JournalConfig]:
        journal_configs = self.journal_dynamodb_table.query(
            KeyConditionExpression="pK = :pK",
            ExpressionAttributeValues={":pK": "CONFIG"},
        )["Items"]

        return [
            JournalConfig(
                journal_config["payload"]["journal_type"],
                journal_config["payload"]["journal_url"],
                journal_config["payload"]["destination_addresses"],
                journal_config["payload"]["username"],
                journal_config["payload"]["password"],
            )
            for journal_config in journal_configs
        ]

    def get_last_journal_status(self, journal_type: str) -> Optional[PaperStatus]:
        current_ts = int(time.time() * 1000)
        last_journal_status = self.journal_dynamodb_table.query(
            KeyConditionExpression="pK = :pK AND #timestamp < :timestamp",
            ExpressionAttributeValues={
                ":pK": f"STATUS#{journal_type}",
                ":timestamp": current_ts,
            },
            ExpressionAttributeNames={"#timestamp": "timestamp"},
            ScanIndexForward=False,
            Limit=1,
        )["Items"]

        if not last_journal_status:
            return None

        return PaperStatus(
            last_journal_status[0]["payload"]["title"],
            last_journal_status[0]["payload"]["step"],
            last_journal_status[0]["payload"]["status"],
            last_journal_status[0]["payload"]["status_date"],
            last_journal_status[0]["payload"]["link"],
        )

    def save_journal_status(self, journal_type: str, paper_status: PaperStatus) -> None:
        current_ts = int(time.time() * 1000)
        self.journal_dynamodb_table.put_item(
            Item={
                "pK": f"STATUS#{journal_type}",
                "timestamp": current_ts,
                "payload": paper_status.__dict__,
            }
        )
