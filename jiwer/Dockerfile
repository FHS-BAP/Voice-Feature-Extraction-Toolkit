FROM registry.access.redhat.com/ubi8/ubi:latest
RUN yum -y update && \ 
    yum -y install python3.9 && \
    yum -y install git
WORKDIR /scripts
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install jiwer
