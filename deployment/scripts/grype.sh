#!/bin/bash

yum install tar gzip -y > logs.txt
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
grype .
