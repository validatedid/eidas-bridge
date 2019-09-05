#!/bin/bash

# set ServerName variable
echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Start apache
apache2ctl start 

# Start eIDAS web demo
python3 /code/demo/eidas_start_demo.py