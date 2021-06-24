#!/bin/sh -l
context='{"repository":"$1","ref":"$2","actor":"$3","run_id":"$4","sha":"$5"}'
python /main.py --context $context --tool $6 --input-file $7 --output-file $8 --renderer $9
