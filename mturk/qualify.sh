#!/bin/sh
source ~/.aws_credentials_XXXX
aws mturk associate-qualification-with-worker --qualification-type-id XXXXXXXXX --worker-id XXXXXX --integer-value 1 --no-send-notification
aws mturk associate-qualification-with-worker --qualification-type-id TYYYYYYTT --worker-id XXXXXX --integer-value 1 --no-send-notification

