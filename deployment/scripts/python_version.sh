#!/bin/bash
set -x

yum install python311 -y

python3.11 -m ensurepip --upgrade

python3.11 -m pip install --upgrade pip

python3.11 -m pip install wheel
