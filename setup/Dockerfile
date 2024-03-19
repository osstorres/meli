FROM python:3.11-alpine
RUN apk --no-cache add zip jq aws-cli

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY setup/entrypoint.sh /app/entrypoint.sh
COPY lambda_consumer/ .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
