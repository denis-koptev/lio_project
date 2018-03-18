#!/bin/sh

# To identify that docker target started we will create file with target ip in session mounted folder
echo `hostname -I | cut -d' ' -f1` > /lio_project/session/target_ip
