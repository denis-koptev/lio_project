#!/bin/sh

# First edit initiatorname and connect to tgt

touch /lio_project/session/$1_devs
lsscsi > /lio_project/session/$1_devs

# TODO: Write all logic and relax :)
