#!/bin/bash

service mysql start

python scraper.py

uvicorn main:app --host