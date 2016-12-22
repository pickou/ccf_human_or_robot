#!/bin/bash

./lightgbm config=train.conf
./lightgbm config=predict.conf
#python ./split_result.py
#zip high_result.zip high_result.csv
