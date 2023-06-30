#!/bin/bash

python3 -m pip install --user virtualenv
python -m virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt

echo -e "To activate the virtual envarontment run: \n`source ./venv/bin/activate`\n"
