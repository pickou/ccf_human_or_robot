import pandas as pd
from pandas import DataFrame

TYPE = ['train', 'test']

INPUTS = [r'../data/{0}_need.csv',
          r'../data/{0}_ip_cookie_stat.csv',
          r'../data/{0}_media.csv',
          r'../data/{0}_platform.csv',
          r'../data/{0}_cookie_fdt.csv',
          r'../data/{0}_cookie_camp_stat.csv',
          r'../data/ip_fdt_{0}.csv',
          r'../data/{0}_ip_camp_stat.csv']

COL_TYPE = [{'rank':int, 'dt':int, 'camp_id':int, 'creative_id':int,
             'has_ua':int, 'media_id':int, 'label':int},
            {'rank':int, 'ip_dt':int, 'cookie_dt':int, 'ip_cookie':int, 'label':int},
            {'rank':int, 'media_id':int, 'media_ft':int, 'label':int},
            {'rank':int, 'platform':int, 'label':int},
            {'rank':int,'fdt_mean':float,'fdt_std':float,'label':int},
            {'rank':int, 'dt':int, 'cookie':object, 'camp':int, 'label':int,'camp_dt':int},
            {'rank':int,'ip_fdt_mean':float,'ip_fdt_std':float,'label':int},
            {'rank':int,'ip_camp_dt':int,'label':int}]

OUTPUTS = r'../run/{0}_final.csv'

for T in TYPE:
    inputs = [x.format(T) for x in INPUTS]
    output = OUTPUTS.format(T)
    need = pd.read_csv(inputs[0], dtype=COL_TYPE[0])
    print(need.info())
    for i in range(1, len(inputs)):
        temp = pd.read_csv(inputs[i], dtype=COL_TYPE[i])
        need = pd.merge(need, temp , how='left', on=['rank', 'label'])
    print(need.head())
    #need = need.sort_values(by='rank')
    need = need[['label', 'ip_dt', 'cookie_dt', 'ip_cookie', 'platform', 'media_ft' ,'fdt_mean','fdt_std','camp_dt','ip_camp_dt','ip_fdt_mean','ip_fdt_std']]

    need.to_csv(output, header=False, index=False)
