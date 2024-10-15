#!/usr/bin/env bash

conda create -n cs229 python=3.12
conda activate cs229

conda install -n cs229 pytorch tqdm sklearn scikit-learn