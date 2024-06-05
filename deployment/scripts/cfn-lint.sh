#!/bin/bash
set -x

pip install cfn-lint > logs.txt
cfn-lint template.yaml; exit_status=$?

ERROR_MASK=2
WARNING_MASK=4
INFO_ERROR_MASK=8

if [ $(( exit_status & ERROR_MASK )) -gt 0 ]
then
  echo "Errors!" >&2
  # Fail on errors
  exit 1
elif [ $(( exit_status & WARNING_MASK )) -gt 0 ]
then
  echo "Warnings!" >&2
  # Don't fail on warnings
  exit 0
elif [ $(( exit_status & INFO_ERROR_MASK )) -gt 0 ]
then
  echo "Info" >&2
  # Don't fail on info
  exit 0
else
  exit 0
fi
