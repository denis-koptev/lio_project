FROM deniskoptev/jenkins_persistent
MAINTAINER Denis Koptev

USER root

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install --yes python3
RUN apt-get install --yes python3-pip
RUN pip3 install pycodestyle

