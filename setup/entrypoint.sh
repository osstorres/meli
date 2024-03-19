#!/bin/sh

export AWS_ACCESS_KEY_ID=DUMMYIDEXAMPLE
export AWS_SECRET_ACCESS_KEY=DUMMYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1
export DYNAMODB_ENDPOINT=http://dynamodb-local:8000
export SQS_ENDPOINT=http://localstack:4566
export DYNAMODB_TABLE_NAME=stats
export SQS_QUEUE_URL=http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/stats_queue


cat <<EOF > admin-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF

echo "Create admin"
aws \
 --endpoint-url=http://localstack:4566 \
 --region us-east-1 \
 iam create-role \
 --role-name admin-role \
 --path / \
 --assume-role-policy-document file://admin-policy.json

echo "Make S3 bucket"
aws \
  s3 mb s3://lambda-functions \
  --endpoint-url http://localstack:4566

echo "Create SQS queue stats_queue"
aws \
  sqs create-queue \
  --queue-name stats_queue \
  --endpoint-url http://localstack:4566 \
  --region us-east-1

echo "Create DynamoDB table"
aws \
  dynamodb create-table \
  --table-name $DYNAMODB_TABLE_NAME \
  --attribute-definitions \
    AttributeName=date_key,AttributeType=S \
  --key-schema \
    AttributeName=date_key,KeyType=HASH \
  --provisioned-throughput \
    ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --endpoint-url $DYNAMODB_ENDPOINT

echo "Generating Lambda function ZIP"
zip -r lambda_consumer.zip lambda.py requirements.txt

echo "Initialize lambda lambda_consumer_test"
aws \
  s3 cp lambda_consumer.zip s3://lambda-functions \
  --endpoint-url http://localstack:4566

aws \
  lambda create-function \
  --endpoint-url=http://localstack:4566 \
  --region us-east-1 \
  --function-name lambda_consumer_test \
  --role arn:aws:iam::000000000000:role/admin-role \
  --handler lambda.handler \
  --runtime python3.11 \
  --description "SQS Lambda handler for test sqs." \
  --timeout 60 \
  --memory-size 128 \
  --code S3Bucket=lambda-functions,S3Key=lambda_consumer.zip \
  --environment Variables="{DYNAMODB_ENDPOINT=$DYNAMODB_ENDPOINT,SQS_ENDPOINT=$SQS_ENDPOINT,DYNAMODB_TABLE_NAME=$DYNAMODB_TABLE_NAME,AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION,AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY,SQS_QUEUE_URL=$SQS_QUEUE_URL}"

aws \
  lambda create-event-source-mapping \
  --function-name lambda_consumer_test \
  --batch-size 1 \
  --event-source-arn "arn:aws:sqs:us-east-1:000000000000:stats_queue" \
  --region us-east-1 \
  --endpoint-url=http://localstack:4566

echo "All resources initialized! 🚀"
