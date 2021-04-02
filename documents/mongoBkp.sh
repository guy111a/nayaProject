#!/usr/bin/bash
mongodump --db  bigData --collection cellData --host xaviercat.com  -u user -p 2020P --authenticationDatabase bigData --gzip --archive > /tmp/cellData_dump_`date "+%Y-%m-%d-%H-%M"`.gz

/usr/bin/python3 /home/guy/Documents/moveMongo2gcp.py
