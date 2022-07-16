#!/bin/bash

set -e

echo "In build script"
virtualenv --without-pip virtualenv
echo "Ran virtualenv"
pip install -r requirements.txt --target virtualenv/lib/python3.9/site-packages
echo "Ran ran"
