#!/usr/bin/env bash

conda config --add channels conda-forge
conda config --set channel_priority strict
conda install --file requirements.txt -y
