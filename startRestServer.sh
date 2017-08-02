#!/usr/bin/env bash 

source rest_env/Scripts/activate
cd rest_env/tutorial
python3.6 manage.py runserver 0.0.0.0:8081
