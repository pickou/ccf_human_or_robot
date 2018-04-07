import pandas as pd
PUTS = [r'./data/train-stat', r'./data/test-stat']
COL_TYPE={'label':int,'ip_dt':float,'camp_dt':float,'ip_camp_dt':float,'cookie_camp_dt':float,'camp':int}
for f in PUTS:
    raw=pd.read_csv(f,dtype=COL_TYPE)
    raw=raw[['label','ip_dt','camp_dt','ip_camp_dt','cookie_f_dt','camp']]
    raw.to_csv(f,index=False)

