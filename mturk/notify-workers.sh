#!/bin/sh
aws mturk notify-workers --endpoint-url https://mturk-requester-sandbox.us-east-1.amazonaws.com --subject "test_subject" --worker-ids "XXXXXX" --message-text "this is a message"
aws mturk notify-workers --subject "Thank you for your participation!" --worker-ids "XXXXXX" --message-text "Hello, thank you for pointing out a technical issue in the HIT."
aws mturk notify-workers --subject "Thank you for your participation!" --worker-ids "XXXXXX" --message-text "Hello, thank you for your feedback. Yes, in this HIT, it is allowed to use pronouns like him and her."
