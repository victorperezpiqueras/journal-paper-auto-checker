# Journal Paper Auto-Checker

The Dockerfile is built thanks to this [repo](https://github.com/umihico/docker-selenium-lambda). The image goes with these versions:

- Python 3.10.11
- chromium 114.0.5735.0
- chromedriver 114.0.5735.90
- selenium 4.9.1

To define the journals to check, create an entry in the DynamoDB table created as follows:

```json
{
  "pK": "CONFIG",
  "timestamp": 0,
  "payload": {
    "journal": "<JOURNAL_TYPE>",
    "destination_addresses": ["<email1>", "..."],
    "username": "<your username>",
    "password": "<your password>"
  }
}
```

Journal types are defined in `/src/journal_types.py`. The `destination_addresses` field is a list of email addresses to send the report to. The `username` and `password` fields are the credentials to log in to the journal website.
