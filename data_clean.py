import pandas as pd
from pandas import DataFrame
name_index=["rank","dt","cookie","ip","label"]
col_type={'rank':int,'dt':int,'cookie':object,'ip':object,'label':int}
name=['AdMaster_train_dataset','test_data']
choose=0#choose train(0) or test(1)
file_name=['train_data_csv','test_data_csv']
#从7天的日志中统计每天的数据
for i in range(1,8):
    data_needed=pd.read_csv('./{0}/{1}_{2}.csv'.format(file_name[choose],name[choose],i),names=name_index,dtype=col_type)
    #ip在一天内出现的次数
    ip_temp=data_needed[['ip','label']].groupby(['ip'])
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
    cookie_temp=data_needed[['cookie','label']].groupby(['cookie'])
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
    ip_cookie_temp=data_needed[['ip','cookie','label']].groupby(['ip','cookie'])
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
    data_needed.to_csv('./{0}/{0}_to_use_{1}.csv'.format(file_name[choose],i),index=False)
    del data_needed
    print i

