
#!/bin/bash
pip install bandit
bandit app/ -r -c deployment/bandit.yaml 
bandit trigger/ -r -c deployment/bandit.yaml 