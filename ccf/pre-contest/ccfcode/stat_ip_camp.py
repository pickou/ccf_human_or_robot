import pandas as pd
from pandas import DataFrame
COL_TYPE = {'rank':int, 'dt':int, 'ip':object, 'camp_id':int, 'creative_id':int,'label':int}
header=['rank','dt','ip','camp_id','creative_id','label']



INPUTS = [r'../data/ip_camp_train.csv', r'../data/ip_camp_test.csv']
OUTPUTS = [r'../data/train_ip_camp_stat.csv', r'../data/test_ip_camp_stat.csv']

for i in range(0,2):
    raw=pd.read_csv(INPUTS[i],dtype=COL_TYPE,names=header)
    data=raw[['dt','ip','camp_id','creative_id']]

    grouped = data.groupby(['dt', 'ip','camp_id'])
    grouped1=data['dt','ip','camp_id','label'][data['creative_id']==0].groupby(['dt','ip','camp_id'])



    ip_camp_count=(grouped1.count()/grouped.count()).reset_index(level=['dt','ip','camp_id'])
    ip_camp_count.rename(columns={'label':'ip_camp_dt'},inplace=True)
    need = pd.merge(raw, ip_camp_count, how='left',on=['dt', 'ip','camp_id'])
    need = need.sort_values(by='rank')
    need=need[['rank','ip_camp_dt','label']]
    need.to_csv(OUTPUTS[i], index=False)

