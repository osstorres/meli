FROM public.ecr.aws/lambda/python:3.11

WORKDIR /app

COPY requirements.txt .

RUN  pip3 install -r requirements.txt

COPY lambda.py ${LAMBDA_TASK_ROOT}/lambda.py
CMD [ "lambda.handler" ]
