# Journal Paper Auto-Checker

<p align="start">
  <img src="https://img.shields.io/static/v1?label=python&message=v3.10&color=blue">
  <img src="https://img.shields.io/static/v1?label=selenium&message=v4.9.1&color=blue">
  <img src="https://img.shields.io/static/v1?label=serverless-framework&message=v3&color=red">
  <img src="https://img.shields.io/static/v1?label=cloud&message=AWS&color=yellow">
</p>

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
    "journal_type": "<JOURNAL_TYPE>",
    "journal_url": "<journal_url>",
    "destination_addresses": ["<email1>", "..."],
    "username": "<your username>",
    "password": "<your password>"
  }
}
```

Journal scrapers are defined in `/src/models/journal.py`. The `destination_addresses` field is a list of email addresses to send the report to. The `username` and `password` fields are the credentials to log in to the journal website.

# How to set up

Install the serverless framework:

```bash
npm install -g serverless
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Setup AWS credentials, launch docker and deploy:

```bash
serverless deploy
```
