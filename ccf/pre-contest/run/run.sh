#!/bin/bash

./lightgbm config=train.conf
./lightgbm config=predict.conf
python ./split_result.py
