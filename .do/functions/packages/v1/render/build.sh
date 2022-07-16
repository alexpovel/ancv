#!/bin/bash

# set -e

virtualenv --without-pip virtualenv
# pip install --user ancv

pip install -r requirements.txt --target virtualenv/lib/python3.9/site-packages
source virtualenv/bin/activate
# echo "In build script"
# virtualenv --without-pip virtualenv
# echo "Ran virtualenv"
# pip install -r requirements.txt --target virtualenv/lib/python3.9/site-packages
# echo "Ran ran"
