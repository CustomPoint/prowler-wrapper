#!/bin/bash
set -x -e
# There should be an AWS folder in the current directory
# It should contain an AWS "config" file & "credentials" file

# Make sure that the Docker image is generated
docker-compose build

rm -rf ./reports/*
rm -rf accounts_status.log

# Parsing out the profiles and running docker for all of them
grep -E -o "\[(.*)\]" aws/credentials | while read -r line ; do
    line=${line#"["}
    line=${line%"]"}
    echo "Processing Profile: ${line}"
    docker run --rm -v $PWD/reports:/report -v $PWD/aws:/root/.aws -e AWS_PROFILE=${line} prowler 2>&1
    exit 0
done

python3 aggregate_results.py > accounts_status.log