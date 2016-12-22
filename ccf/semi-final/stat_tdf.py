import pandas as pd
from pandas import DataFrame
COL_TYPE0 = {'dt':int, 'cookie':object, 'f':object, 'timestamps':int, 'camp':object,'creative_id':int,'born_time':object,'label':int}
COL_TYPE1 = {'row_number':int,'dt':int, 'cookie':object, 'f':object, 'timestamps':int, 'camp':object,'creative_id':int,'born_time':object,'label':int}
header0=['dt','cookie','f','timestamps','camp','creative_id','born_time','label']
header1=['row_number','dt','cookie','f','timestamps','camp','creative_id','born_time','label']


INPUTS_train = [r'./data/train_ip_camp_{0}.csv'.format(i) for i in range(0,3)]
INPUTS_test =[r'./data/test_ip_camp_{0}.csv'.format(i) for i in range(0,2)]
OUTPUTS_ = [[r'./data/train-tdf_{0}'.format(i) for i in range(0,3)],[ r'./data/test-tdf_{0}'.format(i) for i in range(0,2)]]

for i in range(0,2):
    k=0
    if(i==0):
        COL_TYPE=COL_TYPE0
        INPUTS=INPUTS_train
        OUTPUTS=OUTPUTS_[0]
    else:
        COL_TYPE=COL_TYPE1
        INPUTS=INPUTS_test
        OUTPUTS=OUTPUTS_[1]
    for f in INPUTS:
        raw=pd.read_csv(f,dtype=COL_TYPE)
        print "csv read success!"
        raw=raw[['cookie','timestamps']]
        #cookie_timestamps

        data=raw[['cookie','timestamps']]
        cookie_timestamps=data.groupby(['cookie'])
        del data,raw
        #cookie_fdt={"cookie":[],"fdt_mean":[],"fdt_std":[]}
        tf=cookie_timestamps.diff()
        del cookie_timestamps
        #tf['timestamps'].fillna(0,inplace=True)
        print tf.head()
        tf.to_csv(OUTPUTS[k],index=False)
        k=k+1
'''
        for b,group in cookie_timestamps:
            cookie_fdt['cookie'].append(b)
            cookie_fdt['fdt_mean'].append(group['timestamps'].diff().mean())
            cookie_fdt['fdt_std'].append(group['timestamps'].diff().std())
        df=DataFrame(cookie_fdt)
        need=pd.merge(data,df,how='left',on=['cookie'],sort=False)

        need['fdt_mean'].fillna(need['fdt_mean'].mean(),inplace=True)
        need['fdt_std'].fillna(need['fdt_std'].mean(),inplace=True)

        need=need[['fdt_mean','fdt_std']]
        print need.head()
        need.to_csv(OUTPUTS[k], index=False)
        k=k+1
    del need,raw,last_need
'''
