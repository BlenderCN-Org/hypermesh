#!/usr/bin/bash

set -e
flake8 --count --exclude=./addon/__init__.py .
flake8 --count --ignore F401,E402,F821 ./addon/__init__.py

