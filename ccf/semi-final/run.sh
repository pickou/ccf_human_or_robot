#!/bin/bash


#cd /home/era/Documents/my_workplace/ccf/origin/
#tar zxf ccf_data_1.tar.gz
#tar zxf ccf_data_2.tar.gz
#tar zxf ccf_data_3.tar.gz
#tar zxf test_data_1_1118.tar.gz
#tar zxf test_data_2_1118.tar.gz

###################################
# merge train data
###################################
#cp ccf_data_1 train
#cat ccf_data_2 >> train
#cat ccf_data_3 >> train

###################################
# merge test data
###################################
#cp test_data_1_1118 test
#cat test_data_2_1118 >> test

cd /home/era/Documents/my_workplace/zhou
#python  select_data.py
#python stat.py
#python stat_camp_cookie.py
#python choose_feature.py
#python processing.py

cd ./lightgbm
./run.sh

cd ../
python split_result.py
