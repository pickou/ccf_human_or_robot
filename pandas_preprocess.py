import pandas as pd
from pandas import DataFrame
test_name_index=["rank","dt","cookie","ip","idfa","imei","android","openudid",\
                  "mac","timestamps","camp","creativeid","mobile_os","mobile_type",\
                  "app_key_md5","app_name_md5","placementid","useragent","mediaid",\
                  "os_type","born_time"]
train_name_index=test_name_index+["label"]
train_data=pd.read_csv(r'D:\\AdMaster_competition_dataset\AdMaster_train_dataset_3000000_0.csv',\
                       names=train_name_index)
#统计缺失值
print train_data.isnull().sum()
#去掉缺失值
train_data_notnull=train_data.drop(['idfa','imei','android','openudid','mac','mobile_os','mobile_type',\
                                    'app_key_md5','app_name_md5','useragent','os_type'],axis=1)
#查看有效值的信息
print train_data_notnull.info()
#重新写入csv
train_data_notnull.to_csv(r'D:\\AdMaster_competition_dataset\train_data_3000000.csv')
