#!/bin/bash

set -e

# Ensure user has virtualenv installed
virtualenv --version
pip --version

virtualenv env
source env/bin/activate

# Use pip to install the tmuxp package in the virtualenv
pip install tmuxp jinja2

deactivate
