attributes = [
'rank',                 # 0
'dt',                   # 1
'cookie',               # 2
'ip',                   # 3
'mobile_idfa',          # 4
'mobile_imei',          # 5
'mobile_android_id',    # 6
'mobile_openudid',      # 7
'mobile_mac',           # 8
'timestamps',           # 9
'camp_id',              # 10
'creative_id',          # 11
'mobile_os',            # 12
'mobile_type',          # 13
'mobile_app_key',       # 14
'mobile_app_name',      # 15
'placement_id',         # 16
'user_agent',           # 17
'media_id',             # 18
'os',                   # 19
'cookie_born_time',     # 20
'label',                # 21
]

INPUTS = [r'../data/AdMaster_train_dataset.csv', r'../data/final_ccf_test_0919.csv']
OUTPUTS = [r'../data/train_cookie_timestamps.csv', r'../data/test_cookie_timestamps.csv']

SELECTED = [0, 1, 2, 9, 20,21]

#header = [attributes[x] for x in SELECTED]

for i in range(0, 2):
    saved = open(OUTPUTS[i], 'w')
    #saved.write(','.join(header)+'\n') # write header

    with open(INPUTS[i], 'r') as origin:
        while True:
            lines = origin.readlines(10000)
            if not lines:
                break
            for line in lines:
                line = line.split(',')
                instance = [line[x] for x in SELECTED]
                instance = ','.join(instance) # label has a '\n'
                saved.write(instance)

    saved.close()
