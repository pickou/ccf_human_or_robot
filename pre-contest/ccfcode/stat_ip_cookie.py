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

INPUTS = [r'../data/train_ip_cookie_raw.csv', r'../data/test_ip_cookie_raw.csv']
OUTPUTS = [r'../data/train_ip_cookie_stat.csv', r'../data/test_ip_cookie_stat.csv']

#header = ['rank', 'ip_dt', 'cookie_dt', 'ip_cookie', 'label']

COL_TYPE = {'rank':int, 'dt':int, 'cookie':object, 'ip':object, 'label':int}

for i in range(0, 2):
    raw = pd.read_csv(INPUTS[i], dtype=COL_TYPE)

    data = raw[['dt', 'ip', 'label']]
    ip_dt_count = data.groupby(['dt', 'ip']).count().reset_index(level=['dt','ip'])
    ip_dt_count.rename(columns={'label':'ip_dt'}, inplace=True)
    print("ip_dt_count success")
    data = raw[['dt', 'cookie', 'label']]
    cookie_dt_count = data.groupby(['dt', 'cookie']).count().reset_index(level=['dt','cookie'])
    cookie_dt_count.rename(columns={'label':'cookie_dt'}, inplace=True)
    print("cookie_dt_count success")
    data = raw[['dt','cookie', 'ip', 'label']]
    ip_cookie_count = data.groupby(['dt','cookie', 'ip']).count().reset_index(level=['dt','cookie','ip'])
    ip_cookie_count.rename(columns={'label':'ip_cookie'}, inplace=True)
    print("ip_cookie_count success")
    need = pd.merge(raw, ip_dt_count, on=['dt', 'ip'])
    need = pd.merge(need, cookie_dt_count, on=['dt', 'cookie'])
    need = pd.merge(need, ip_cookie_count, on=['dt','cookie', 'ip'])

    need = need[['rank', 'ip_dt', 'cookie_dt', 'ip_cookie', 'label']]
    need = need.sort_values(by='rank')
    need.to_csv(OUTPUTS[i], index=False)
