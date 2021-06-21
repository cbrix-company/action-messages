#!/bin/sh -l
python /main.py --slack-channel-id $2 --slack-token $1 --output-file $3 --repo-name $4
