#attributes = [
#'rank',                 # 0
#'dt',                   # 1
#'cookie',               # 2
#'ip',                   # 3
#'mobile_idfa',          # 4
#'mobile_imei',          # 5
#'mobile_android_id',    # 6
#'mobile_openudid',      # 7
#'mobile_mac',           # 8
#'timestamps',           # 9
#'camp_id',              # 10
#'creative_id',          # 11
#'mobile_os',            # 12
#'mobile_type',          # 13
#'mobile_app_key',       # 14
#'mobile_app_name',      # 15
#'placement_id',         # 16
#'user_agent',           # 17
#'media_id',             # 18
#'os',                   # 19
#'cookie_born_time',     # 20
#'label',                # 21
#]

import pandas as pd
from pandas import DataFrame

INPUTS = [r'../data/cookie_camp_train.csv', r'../data/cookie_camp_test.csv']
OUTPUTS = [r'../data/train_cookie_camp_stat.csv', r'../data/test_cookie_camp_stat.csv']

header = ['rank', 'dt', 'cookie', 'camp', 'label']

COL_TYPE = {'rank':int, 'dt':int, 'cookie':object, 'camp':int, 'label':int}

for i in range(0, 2):
    raw = pd.read_csv(INPUTS[i], dtype=COL_TYPE,names=header)
    data=raw[['dt', 'cookie', 'camp', 'label']]
    camp_dt_count = data.groupby(['dt', 'cookie','camp']).count().reset_index(level=['dt','cookie','camp'])
    camp_dt_count.rename(columns={'label':'camp_dt'}, inplace=True)
    need = pd.merge(raw, camp_dt_count, how='left',on=['dt', 'cookie','camp'])
    need = need.sort_values(by='rank')
    print need.head()
    need.to_csv(OUTPUTS[i], index=False)
