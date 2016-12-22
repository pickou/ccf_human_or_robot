import pandas as pd
from pandas import DataFrame
TYPE=['train','test']
COL_TYPE = {"rank":int,"dt":int,"cookie":object,'timestamps':int,'cookie_born_time':object,'label':int}
#header = ['rank', 'dt', 'cookie','timestamps','cookie_born_time','label']
for T in TYPE:
    cookie_fdt={"cookie":[],"cookie_born_time":[],"fdt_mean":[],"fdt_std":[]}
    raw=pd.read_csv('../data/{0}_cookie_timestamps.csv'.format(T),dtype=COL_TYPE)
    cookie_timestamps=raw[['cookie_born_time','cookie','timestamps']].groupby(['cookie_born_time','cookie'])
    for (b,cookie),group in cookie_timestamps:
        cookie_fdt["cookie"].append(cookie)
        cookie_fdt["cookie_born_time"].append(b)
        cookie_fdt["fdt_mean"].append(group['timestamps'].diff().mean())
        cookie_fdt['fdt_std'].append(group['timestamps'].diff().std())
    df=DataFrame(cookie_fdt)
    df=pd.merge(raw,df,on=['cookie','cookie_born_time'])
    df=df[['rank','fdt_mean','fdt_std','label']]
    df=df.sort_values(by='rank')
    df['fdt_mean'].fillna(df['fdt_mean'].max(),inplace=True)
    df['fdt_std'].fillna(df['fdt_std'].min(),inplace=True)

    df.to_csv('../data/{0}_cookie_fdt.csv'.format(T),index=False)
