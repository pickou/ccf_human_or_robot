import pandas as pd
from pandas import DataFrame
COL_TYPE0 = {'dt':object, 'cookie':object, 'f':object, 'timestamps':int, 'camp':object,'creative_id':int,'born_time':object,'label':int}
COL_TYPE1 = {'row_number':int,'dt':object, 'cookie':object, 'f':object, 'timestamps':int, 'camp':object,'creative_id':int,'born_time':object,'label':int}
header0=['dt','cookie','f','timestamps','camp','creative_id','born_time','label']
header1=['row_number','dt','cookie','f','timestamps','camp','creative_id','born_time','label']


INPUTS_train = [r'./data/train_ip_camp_{0}.csv'.format(i) for i in range(0,3)]
INPUTS_test =[r'./data/test_ip_camp_{0}.csv'.format(i) for i in range(0,2)]
OUTPUTS = [r'./data/train-stat', r'./data/test-stat']

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

        data=raw[['dt','f','camp','label']]
        #ip_camp_dt
        ip_camp_dt = data.groupby(['dt', 'f','camp']).count().reset_index(level=['dt', 'f','camp'])
        ip_camp_dt.rename(columns={'label':'ip_camp_dt'}, inplace=True)
        need = pd.merge(raw, ip_camp_dt, how='left',on=['dt', 'f','camp'],sort=False)
        del ip_camp_dt
        print "calculate ip_camp_dt done!"
        #camp_dt
        data=raw[['dt','camp','label']]
        camp_dt=data.groupby(['dt','camp']).count().reset_index(level=['dt','camp'])
        camp_dt.rename(columns={'label':'camp_dt'}, inplace=True)
        need=pd.merge(need,camp_dt,how='left',on=['dt','camp'],sort=False)
        del camp_dt
        print "calculate camp_dt done!"
        #ip_dt
        data=raw[['dt','f','label']]
        ip_dt=data.groupby(['dt','f']).count().reset_index(level=['dt','f'])
        ip_dt.rename(columns={'label':'ip_dt'},inplace=True)
        need=pd.merge(need,ip_dt,how='left',on=['dt','f'],sort=False)
        del ip_dt
        print "calculate ip_dt done!"
        #cookie_dt
        data=raw[['dt','cookie','label']]
        cookie_dt=data.groupby(['dt','cookie']).count().reset_index(level=['dt','cookie'])
        cookie_dt.rename(columns={'label':'cookie_dt'}, inplace=True)
        need=pd.merge(need,cookie_dt,how='left',on=['dt','cookie'],sort=False)
        del cookie_dt
        print "calculate cookie_dt done!"
        #cookie_f
        data=raw[['cookie','f','label']]
        cookie_f=data.groupby(['cookie','f']).count().reset_index(level=['cookie','f'])
        cookie_f.rename(columns={'label':'cookie_f_dt'},inplace=True)
        del raw
        need=pd.merge(need,cookie_f,how='left',on=['cookie','f'],sort=False)
        del cookie_f
        '''
        #cookie_camp_ct
        data=raw[['dt','cookie','camp','born_time']]
        data['bt']=0#identify the cookie borned in dt
        data['bt'].loc[data['dt']==data['born_time']]=1
        cookie_camp_ct=data[['camp','bt']].groupby(['camp']).sum().reset_index(level=['camp'])
        cookie_camp_ct.rename(columns={'bt':'cookie_camp_ct'},inplace=True)
        need=pd.merge(need,cookie_camp_ct,how='left',on=['camp'],sort=False)
        '''
        need=need[['label','ip_dt','cookie_dt','camp_dt','ip_camp_dt','cookie_f_dt','camp']]
        if(flag==1):
            need=pd.concat([last_need,need])
        last_need=need
        flag=1
        print need.head()
    need.to_csv(OUTPUTS[i], index=False)
    del need,last_need
