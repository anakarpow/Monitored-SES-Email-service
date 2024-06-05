#!/bin/bash
pip install bandit
bandit app/  -r -c deployment/bandit.yaml  --severity-level high

bandit trigger/  -r -c deployment/bandit.yaml  --severity-level high
