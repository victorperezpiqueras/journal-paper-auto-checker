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

To define a journal to check, create an entry in the created DynamoDB table with the data structure defined in `src/infrastructure/sample_config.json`.

Journal scrapers are defined in `/src/domain/journal.py`. The `destination_addresses` field is a list of email addresses to send the report to. The `username` and `password` fields are the credentials to log in to the journal website.

The entry-point of the cron lambda function is `/src/application/cron_checker.py`.

The email format is defined in `/src/domain/email_formatter.py`.

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
