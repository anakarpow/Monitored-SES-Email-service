#!/bin/bash
pip install bandit
bandit cost-reporting/  -r -c deployment/bandit.yaml  --severity-level high

bandit metering/  -r -c deployment/bandit.yaml  --severity-level high

bandit cast_package/  -r -c deployment/bandit.yaml  --severity-level high
