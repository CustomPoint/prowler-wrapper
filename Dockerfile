FROM python:2.7-slim

WORKDIR /root

# install prerequisites
RUN apt update
RUN apt install -y unzip
RUN pip install awscli
# this is necessary for the aws cli - groff needs to be available
RUN apt-get install --reinstall groff-base 
RUN apt install -y wget curl

# copy the aws folder into the .aws default directory
COPY aws/* /root/.aws/
COPY entrypoint.sh /root/entrypoint.sh

# setting up prowler for it to be a RUN command
RUN wget https://github.com/Alfresco/prowler/archive/master.zip
RUN unzip master.zip -d /root/
# RUN cp /root/prowler-master/prowler /usr/bin/
RUN mkdir -p /report
ENTRYPOINT /bin/bash /root/entrypoint.sh 