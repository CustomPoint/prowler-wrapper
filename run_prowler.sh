#!/usr/bin/env bash
echo "== This will prowl through your AWS accounts and force you to fix the issues !!!"
echo "= Analysing accounts..."
/bin/bash ./analyse_accounts.sh 2>&1 > /dev/null

echo "= Waiting for the analysis to finish..."
sleep 5
docker ps | grep prowler 
echo $?
while [ $? -eq 0 ] ;
do
    docker ps | grep prowler 2>&1 > /dev/null
done
echo "= Analysis is DONE!"
echo "= Aggregating the results and generating the output..."
python3 aggregate_results.py > accounts_status.log

echo "== DONE!"