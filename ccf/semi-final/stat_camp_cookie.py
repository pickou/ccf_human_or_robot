import pandas as pd
from pandas import DataFrame
COL_TYPE0 = {'dt':int, 'cookie':object, 'f':object, 'timestamps':int, 'camp':object,'creative_id':int,'born_time':int,'label':int}
COL_TYPE1 = {'row_number':int,'dt':int, 'cookie':object, 'f':object, 'timestamps':int, 'camp':object,'creative_id':int,'born_time':int,'label':int}
header0=['dt','cookie','f','timestamps','camp','creative_id','born_time','label']
header1=['row_number','dt','cookie','f','timestamps','camp','creative_id','born_time','label']


INPUTS_train = [r'./data/train_ip_camp_{0}.csv'.format(i) for i in range(0,3)]
INPUTS_test =[r'./data/test_ip_camp_{0}.csv'.format(i) for i in range(0,2)]
OUTPUTS = [r'./data/train-camp_cookie_stat', r'./data/test-camp_cookie_stat']

for i in range(0,2):
    flag=0
    if(i==0):
        COL_TYPE=COL_TYPE0
        INPUTS=INPUTS_train
    else:
        COL_TYPE=COL_TYPE1
        INPUTS=INPUTS_test
    for f in INPUTS:
        raw=pd.read_csv(f,dtype=COL_TYPE)

        print "csv read success!"

        #cookie_camp_ct
        data=raw[['dt','cookie','camp','born_time']]
        data['bt']=0#identify the cookie borned in dt
        data['bt'].loc[data['dt']==data['born_time']]=1
        cookie_camp_ct=data[['camp','bt']].groupby(['camp']).sum().reset_index(level=['camp'])
        cookie_camp_ct0=data[['camp','cookie','bt']].groupby(['camp','cookie']).count().reset_index(level=['camp','cookie'])

        cookie_camp_ct0.rename(columns={'bt':'cookie_camp_ct0'},inplace=True)
        cookie_camp_ct.rename(columns={'bt':'cookie_camp_ct'},inplace=True)
        need=pd.merge(data,cookie_camp_ct,how='left',on=['camp'],sort=False)
        need=pd.merge(need,cookie_camp_ct0,how='left',on=['camp','cookie'],sort=False)
        need['cookie_camp_rt']=0
        need['cookie_camp_rt']=need['cookie_camp_ct']-need['cookie_camp_ct0']+1#cal. the rate of new born cookie
        need=need[['cookie_camp_ct']]
        print need.head()
        if(flag==1):
            need=pd.concat([last_need,need])
        last_need=need
        flag=1
        #print need.head()
    need.to_csv(OUTPUTS[i], index=False)
    del need,raw,last_need
