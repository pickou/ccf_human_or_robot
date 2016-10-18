import pandas as pd
from pandas import DataFrame
test_name_index=["rank","dt","cookie","ip","idfa","imei","android","openudid",\
                  "mac","timestamps","camp","creativeid","mobile_os","mobile_type",\
                  "app_key_md5","app_name_md5","placementid","useragent","mediaid",\
                  "os_type","born_time"]
train_name_index=test_name_index+["label"]
test_name_index=["rank","dt","cookie","ip","idfa","imei","android","openudid",\
                  "mac","timestamps","camp","creativeid","mobile_os","mobile_type",\
                  "app_key_md5","app_name_md5","placementid","useragent","mediaid",\
                  "os_type","born_time"]
test_type={'rank':int,'dt':int,'cookie':object,'ip':object,'idfa':object,'imei':object,\
            'android':object,'openudid':object,'mac':object,'timestamps':int,'camp':int,\
            'creativeid':int,'mobile_os':object,'mobile_type':object,'app_key_md5':object,\
            'app_name_md5':object,'placementid':object,'useragent':object,'mediaid':int,\
            'os_type':object,'born_time':int}
train_type=dict({'label':int},**test_type)
#从7天的日志中统计每天的数据
for i in range(1,8):
    pd_file=pd.read_csv('AdMaster_train_dataset_1000000_{0}.csv'.format(i),names=train_name_index,dtype=train_type )
    data_needed=pd_file[['rank','ip','cookie','label']]
    #ip在一天内出现的次数
    ip_temp=pd_file[['ip','label']].groupby(['ip'])
    ip_count=ip_temp.count()
    #同一个ip作弊的次数
    ip_cheat=ip_temp.sum()
    ip_count=ip_count.reset_index(level=['ip'])
    #rename
    ip_count.rename(columns={'label':'ip_count'},inplace=True)
    #通过merge写回统计好的数据
    data_needed=pd.merge(data_needed,ip_count,on='ip')
    #按照rank排序
    data_needed=data_needed.sort_values(by='rank')
    #从内存中把不需要的数据删除
    del ip_temp,ip_count
    #cookie在一天内出现的次数
    cookie_temp=pd_file[['cookie','label']].groupby(['cookie'])
    cookie_count=cookie_temp.count()
    #同一个cookie作弊的次数
    cookie_cheat=cookie_temp.sum()
    cookie_count=cookie_count.reset_index(level=['cookie'])
    cookie_count.rename(columns={'label':'cookie_count'},inplace=True)
    data_needed=pd.merge(data_needed,cookie_count,on='cookie')
    data_needed=data_needed.sort_values(by='rank')
    #从内存中把不需要的数据删除
    del cookie_temp,cookie_count
    #ip_cookie出现的次数
    ip_cookie_temp=pd_file[['ip','cookie','label']].groupby(['ip','cookie'])
    ip_cookie_count=ip_cookie_temp.count()
    ip_cookie_cheat=ip_cookie_temp.sum()
    #将grouby之后的index还原为column
    ip_cookie_count=ip_cookie_count.reset_index(level=['ip','cookie'])
    #rename label ip_cookie_count,because this is count for ip_cookie
    ip_cookie_count.rename(columns={'label':'ip_cookie_count'},inplace=True)
    data_needed=pd.merge(data_needed,ip_cookie_count,on=['ip','cookie'])
    data_needed=data_needed.sort_values(by='rank')
    #if you don‘t need ip just drop it
    data_needed.drop(['ip','cookie'],axis=1,inplace=True)
    data_needed.to_csv('data_to_use{0}.csv'.format(i))

