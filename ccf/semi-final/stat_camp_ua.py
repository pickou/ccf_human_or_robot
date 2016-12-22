import pandas as pd
from pandas import DataFrame
COL_TYPE0 = {'dt':int, 'camp':object,'user_agent':object,'label':int}
COL_TYPE1 = {'row_number':int,'dt':int,'camp':object,'user_agent':object,'label':int}
header0=['dt','camp','user_agent','label']
header1=['row_number','dt','camp','user_agent','label']


INPUTS_train = [r'./data/train_ua_camp_{0}.csv'.format(i) for i in range(0,3)]
INPUTS_test =[r'./data/test_ua_camp_{0}.csv'.format(i) for i in range(0,2)]
OUTPUTS = [r'./data/train-camp_ua_stat', r'./data/test-camp_ua_stat']

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
        #ua_camp_dt

        data=raw[['camp','user_agent','label']]
        ua_camp_dt=data.groupby(['camp','user_agent']).count().reset_index(level=['camp','user_agent'])
        ua_camp_dt.rename(columns={'label':'ua_camp_dt'},inplace=True)

        need=pd.merge(raw,ua_camp_dt,how='left',on=['camp','user_agent'],sort=False)
        del ua_camp_dt
        need=need[['ua_camp_dt']]
        need.fillna(0,inplace=True)
        if(flag==1):
            need=pd.concat([last_need,need])
        last_need=need
        flag=1
        print need.head()
    need.to_csv(OUTPUTS[i], index=False)
    del need,raw,last_need
