FROM public.ecr.aws/lambda/python:3.11

WORKDIR /app

COPY requirements.txt .

ENV DYNAMODB_ENDPOINT=http://dynamodb-local:8000
ENV SQS_ENDPOINT=http://localstack:4566
ENV DYNAMODB_TABLE_NAME=stats
ENV AWS_DEFAULT_REGION=us-east-1
ENV AWS_ACCESS_KEY_ID=DUMMYIDEXAMPLE
ENV AWS_SECRET_ACCESS_KEY=DUMMYEXAMPLEKEY
ENV SQS_QUEUE_URL=http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/stats_queue

RUN  pip3 install -r requirements.txt

COPY lambda.py ${LAMBDA_TASK_ROOT}/lambda.py
CMD [ "lambda.handler" ]
