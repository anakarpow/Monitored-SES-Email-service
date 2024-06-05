#!/bin/bash

set -x

# install CFN-nag
yum install ruby ruby-devel gcc -y > logs.txt

gem install cfn-nag > logs.txt

cfn_nag_scan --input-path template.yaml
