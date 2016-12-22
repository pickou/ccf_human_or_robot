#!/bin/bash
#python train2test.py
cd ./lightgbm
./lightgbm config=predict.conf
cd ..
python split_result.py
