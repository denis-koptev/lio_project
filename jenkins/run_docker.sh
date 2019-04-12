#!/bin/bash

sudo docker run -p 8080:8080 -p 50000:50000 -v /sys:/sys -v /etc/target:/etc/target -v /var/run/dbus:/var/run/dbus --privileged -d deniskoptev/pytest_lio_jenkins

