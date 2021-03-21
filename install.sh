#!/bin/bash

ENVP=/home/ernst/Desktop/PROJEKTE/prj.PLEISZENBURG.page/env387

source $ENVP/bin/activate

pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements_python.txt
nodeenv -p

deactivate
source $ENVP/bin/activate

npm i -g npm
cat requirements_node.txt | xargs npm install -g

pip instal -e .
