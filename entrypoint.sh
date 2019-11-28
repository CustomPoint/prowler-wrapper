#!/bin/bash

echo "= Starting working with Prowler ..."
if [ -n "$AWS_PROFILE" ];
then
    echo "== Getting the ENV profiles ..."
    /root/prowler-master/prowler -p "$AWS_PROFILE" -M csv > "/report/output-$AWS_PROFILE.csv"
else
    echo "= No ENV defined. Entering console..."
    /bin/bash
fi

echo "= GOODBYE!"