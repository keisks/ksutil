#!/bin/bash
python get_tokens.py |sort |uniq > vocab_10k.txt
