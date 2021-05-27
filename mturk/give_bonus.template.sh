#!/bin/sh

# each line will give a bonus for a specific submission.
aws mturk send-bonus --assignment-id "AAAAAA" --worker-id "AAAAAAA" --bonus-amount "0.01" --reason "REASON for the bonus" --unique-request-token "unique-request-token here (upto 64 chars)"

