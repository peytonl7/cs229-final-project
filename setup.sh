#!/bin/sh
conda init

if conda info --envs | grep -q cs229; 
then echo "environment cs229 already exists";
else conda create -n cs229 python=3.12; 
fi

conda install -n cs229 pytorch tqdm sklearn scikit-learn requests bs4 pandas

conda env config vars set -n cs229 PYTHONPATH=$PWD
