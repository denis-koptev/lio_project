FROM deniskoptev/jenkins_persistent
MAINTAINER Denis Koptev

USER root

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install --yes cppcheck

RUN apt-get install --yes python3
RUN apt-get install --yes python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install pycodestyle jsonschema pep8 pylint pytest-pep8
ADD requirements.txt /
RUN pip3 install -r /requirements.txt

RUN apt-get install --yes targetcli-fb

# Deal with tcmu-runner
ADD install_tcmur_deps.sh /
RUN bash -c "/install_tcmur_deps.sh"

# Temp initiator deps
RUN apt-get install --yes open-iscsi
RUN apt-get install --yes lsscsi
RUN pip3 install -U pytest

