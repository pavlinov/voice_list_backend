#!/bin/bash

export APP=vlb
export STAGE=dev
export S3_BUCKET=cf-templates-1mcysmvkujq2c-us-east-1
export REGION=us-east-1

export SERVICE=databases
export TEMPLATE="aws_templates/databases.yml"

bash ./ci/aws_deploy.sh

