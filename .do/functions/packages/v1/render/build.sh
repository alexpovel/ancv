#!/bin/bash

# set -e

# echo $(whoami)
# whoami

# id

virtualenv virtualenv
source virtualenv/bin/activate
# pip install ancv
pip install -r requirements.txt
deactivate

# virtualenv --without-pip virtualrofl
# pip install --user ancv

# pip install -r requirements --target virtualenv/lib/python3.9/site-packages
# pip install pyjokes --target virtualrofl/lib/python3.9/site-packages
# source virtualenv/bin/activate

# echo "In build script"
# virtualenv --without-pip virtualenv
# echo "Ran virtualenv"
# pip install -r requirements.txt --target virtualenv/lib/python3.9/site-packages
# echo "Ran ran"
