#!/bin/bash
set -e -o pipefail

export PYTHONPATH=".:$(realpath ci):${PYTHONPATH}"

export APP=vlb
export STAGE=dev
export REGION=us-east-1
export AWS_REGION=us-east-1
export S3_BUCKET=cf-templates-1mcysmvkujq2c-us-east-1
export SERVICE=databases
export TEMPLATE="aws_templates/databases.yml"


echo "Debug envs"
env

python ci/put_test_data_in_database.py
