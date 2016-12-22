# convert original data to csv file
# 1. replace '\x01' by ','

attributes = [
'dt',                     # 0
'cookie',                 # 1
'ip',                     # 2
'timestamps',             # 3
'camp',                   # 4
'play',                   # 5
'channel',                # 6
'creative_id',            # 7
'idfa',                   # 8
'mobile_mac',             # 9
'mobile_openudid',        # 10
'imei',                   # 11
'android_id',             # 12
'mobile_os',              # 13
'mobile_type',            # 14
'mobile_app_key',         # 15
'mobile_app_name',        # 16
'placement_id',           # 17
'user_agent',             # 18
'media_id',               # 19
'os_type',                # 20
'born_time',              # 21
'label'                   # 22
]

INPUTS = [r'../origin/ccf_data_{0}'.format(i) for i in range(1,4)]
OUTPUTS = [r'../data/train_dataset.csv', r'../data/test_dataset.csv']
i=0
saved = open(OUTPUTS[0], 'w')
saved.write(','.join(attributes)+'\n') # write header
for f in INPUTS:
    with open(f, 'r') as origin:
        while True:
            lines = origin.readlines(10000)
            if not lines:
                break
            for line in lines:
                saved.write(line)
saved.close()
print line
