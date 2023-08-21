#!/bin/bash

set -e -o pipefail

echo === Environment variables ===
env
echo =============================

aws --version
sam --version

TEMPLATE_FILE="template.yml"
if [[ "$TEMPLATE" != "" ]]; then
  TEMPLATE_FILE=$TEMPLATE
fi

if [[ "$S3_BUCKET" == "" ]]; then
  echo "S3_BUCKET is not set"
  exit 255
fi

if [[ "$STAGE" == "" ]]; then
  echo "STAGE is not set"
  exit 255
fi

if [[ "$REGION" == "" ]]; then
  echo "REGION is not set"
  exit 255
fi


REQUIRED_PARAMS="VLEnvironment=${STAGE} S3Bucket=${S3_BUCKET}"
PARAM_OVERRIDES=${REQUIRED_PARAMS}

STACK_NAME="${APP}-${SERVICE}-${STAGE}"

TAGS="APP=${APP} Stage=${STAGE}"

sam build --use-container --template-file ${TEMPLATE_FILE}

SAM_CAPABILITIES="CAPABILITY_IAM CAPABILITY_AUTO_EXPAND"

set +e -o pipefail

sam deploy i--no-fail-on-empty-changeset \
--on-failure DELETE \
--parameter-overrides ${PARAM_OVERRIDES} \
--tags ${TAGS} \
--s3-bucket=${S3_BUCKET} --stack-name=${STACK_NAME} --capabilities $SAM_CAPABILITIES \
--region=${REGION}
res=$?
echo "Result of the 'sam deploy' operation = ${res}"

STACK_STATUS=$(aws cloudformation describe-stacks --region=${REGION} --stack-name ${STACK_NAME} \
    --query 'Stacks[0].StackStatus' --output text)
echo "STACK_STATUS = $STACK_STATUS"

SUCCESS_REGEX="^(CREATE|UPDATE)_COMPLETE$"
if [[ ${STACK_STATUS} == *"ROLLBACK"* || ${STACK_STATUS} == *"REVIEW_IN_PROGRESS"* || "${STACK_STATUS}" == "" ]]; then
  echo "Pipeline failed: stack in rollback status or does not exist"
  exit 255
fi
