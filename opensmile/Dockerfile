FROM registry.access.redhat.com/ubi8/ubi:latest
RUN yum -y update && \ 
    yum -y install python3.9
WORKDIR /scripts
RUN python3 -m pip install --upgrade pip
RUN yum -y install libsndfile
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt