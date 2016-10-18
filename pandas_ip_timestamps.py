import pandas as pd
from pandas import DataFrame
#import seaborn as sns #ipython notebook allow this
test_name_index=["rank","dt","cookie","ip","idfa","imei","android","openudid",\
                  "mac","timestamps","camp","creativeid","mobile_os","mobile_type",\
                  "app_key_md5","app_name_md5","placementid","useragent","mediaid",\
                  "os_type","born_time"]
train_name_index=test_name_index+["label"]
i=0
for i in range(0,4):
    train_data=pd.read_csv(r'D:\\AdMaster_competition_dataset\train_data_csv\AdMaster_train_dataset_1000000_{0}.csv'.format(i),names=train_name_index,index_col='rank')
    ip_timestamps=train_data[['ip','timestamps','label']]
    if i!=0:
        frames=[ip_timestamps_old,ip_timestamps]
        ip_timestamps=pd.concat(frames)
    ip_timestamps_old=ip_timestamps
    print "the {0}_th run!".format(i)
ip_timestamps.to_csv('ip_timestamps.csv')
'''
    train_data_ip_timestamps=train_data[['ip','timestamps','label']].groupby(['ip'],as_index=False)
    temp=train_data[['ip','label']].groupby(['ip'],as_index=False)
    #a present the cheat rate of the same ip
    a=temp.sum()['label'].astype(float)/temp.count()['label']
    c=temp.sum()['label']
    c_count=c[c!=0].count()
    a_count=a[a==1].count()
    print a_count
    if a_count==c_count:
        print "yes"
    else:
        print a
        print temp.count()['label'][27]
    del temp,train_data,train_data_ip_timestamps
'''
#find the cheat_ip
ip_grouped=ip_timestamps.groupby(['ip'],as_index=False)
ip_grouped_count=ip_grouped.count()
ip_grouped_sum=ip_grouped.sum()
cheat_ip=ip_grouped_sum[['ip']].loc[ip_grouped_sum['label']!=0]
for ip in cheat_ip.values:
    temp1=ip_timestamps[['timestamps']].loc[ip_timestamps['ip']==ip[0]]
    temp1_diff=temp1.diff()
    plt.plot(temp1_diff,'*')
    plt.show()
    k=k+1
    if k==50:
        break
#get the uncheat_ip
    uncheat_ip=ip_grouped_sum[['ip']].loc[ip_grouped_sum['label']==0]
    for ip in uncheat_ip.values:
        temp=ip_timestamps[['timestamps']].loc[ip_timestamps['ip']==ip[0]]
        temp_diff=temp.diff()
        plt.plot(temp_diff,'*')
        plt.show()
        k=k+1
        if k==50:
            break


