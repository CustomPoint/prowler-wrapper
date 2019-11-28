#!/bin/bash
# set -x -e
# There should be an AWS folder in the current directory
# It should contain an AWS "config" file & "credentials" file

# Make sure that the Docker image is generated
docker-compose build
counter=0
# Parsing out the profiles and running docker for all of them
grep -E -o "\[(.*)\]" aws/credentials | while read -r line ; do
    line=${line#"["}
    line=${line%"]"}
    counter=$((counter+1))
    echo "= Processing Profile $counter > ${line}"
    docker run --rm -v $PWD/reports:/report -v $PWD/aws:/root/.aws -e AWS_PROFILE=${line} prowler 2>&1 > /dev/null &
    if [[ "$counter" -eq 5 ]]; then
        counter=0
        echo "= Waiting for the analysis to finish..."
        docker ps | grep prowler
        while [ $? -eq 0 ] ;
        do
            sleep 5
            docker ps | grep prowler 2>&1 > /dev/null
        done
        echo "= Done waiting ... !!"
    fi
done

echo "= Waiting for the analysis to finish..."
docker ps | grep prowler
while [ $? -eq 0 ] ;
do
    sleep 5
    docker ps | grep prowler 2>&1 > /dev/null
done
echo "=== Really DONE waiting !!!"