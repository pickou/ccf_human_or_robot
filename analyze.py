from numpy import *
import pymongo
import pandas as pd
from pandas import DataFrame
#数据库
client=pymongo.MongoClient()
db=client.ccf_robot
test_name_index=["rank","dt","cookie","ip","idfa","imei","android","openudid",\
                  "mac","timestamps","camp","creativeid","mobile_os","mobile_type",\
                  "app_key_md5","app_name_md5","placementid","useragent","mediaid",\
                  "os_type","born_time"]
train_name_index=test_name_index+["label"]

file=open(r'D:\\AdMaster_competition_dataset\final_ccf_test_0919')
#file=open(r'D:\\AdMaster_competition_dataset\AdMaster_train_dataset')
#test_data=[]
for line in file:
    content=line.replace('\n','').split('\x01')
    del line
    a=dict(zip(test_name_index,content))
    db.test.insert_one(a)
