# Email Distribution Service

## Overview

This project implements an AWS Lambda-based service for automated email distribution using Amazon SES. It is designed to process cost reports and send them to a list of recipients, with monitoring and reporting features for internal auditing. The solution is built for CAST and integrates with other Lambda functions for event-driven workflows.

---

## Architecture

- **Trigger:** The Lambda function is triggered by another Lambda (CRC) or scheduled events.
- **Input:** Receives an event containing a list of recipient addresses and metadata (see example below).
- **Processing:**
  - Finds matching cost report files in S3 for each recipient.
  - Sends emails with attachments via SES.
  - Sends a monitoring email to the internal office with sending statistics and a report.
- **Monitoring:** Generates and attaches an HTML report summarizing the sending status.

---

## Event Example

The Lambda expects an event in the following format:

```json
{
    "month": "2023/10/",
    "adresses": [
        {
            "email": "project1@gmail.at", 
            "cost_limit": 5000,
            "project_name": "Water_Bottle_Production",
            "forecast": 67133
        },
        {
            "email": "project999@gmail.at",
            "cost_limit": 10000,
            "project_name": "Cola_Bottle_Production",
            "forecast": 9377
        }
    ]
}
```

---

## Shared Code Between Lambdas

Reusable code is provided in the python directory and packaged as a Lambda Layer (`SharedLayer`). This includes:

- **Email utilities:** Functions for formatting emails, generating monitoring reports, and sending emails with attachments.
- **Monitoring:** HTML report generation for monitoring email status.
- **Address management:** Centralized management of sender/recipient addresses for testing and production.
- **General utilities:** S3 file listing, event processing, and error handling.

To use the shared code in your Lambda, ensure the layer is attached and set the `PYTHONPATH` accordingly.

---

## Testing

### Local Testing

- Test files are located in the SenderFunction directory, e.g.:
  - `test_basic.py`: Tests sending to valid addresses.
  - `test_error.py`: Tests error scenarios (bounces, complaints, invalid addresses).
- Test events and data are in the events directory.
- To run tests locally, set environment variables using env.sh and use `pytest`:

```sh
source env.sh
pytest SenderFunction/
```

### Testing Site

- The project includes a local testing setup with sample events and attachments.
- Use the provided test scripts and sample data to simulate Lambda invocations and verify email delivery and error handling.

---

## Deployment

- Deployment scripts are in scripts.
- The CloudFormation/SAM template is template.yaml.
- Build and deploy using AWS SAM CLI:

```sh
sam build --template template.yaml
sam deploy --config-file deployment/samconfig.toml --config-env dev
```

---

## Security & Compliance

- The Lambda function uses IAM roles with least-privilege permissions for SES and S3.
- Static code analysis and security scanning are integrated into the build pipeline (see `deployment/scripts`).

---

## Goals

- Read incoming event (see `summary_report.json` for example).
- Find matching file in S3.
- Send email with attachment to address.
- Send monitoring email to internal office with sending stats.

---

For more details, see the code and comments in each module.