#!/usr/bin/env bash 

source rest_env/Scripts/activate
cd rest_env/tutorial
python3.6 manage.py runserver 192.168.0.52:8081
