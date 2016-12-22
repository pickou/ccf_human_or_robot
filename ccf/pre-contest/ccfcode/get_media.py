#-*- coding:utf-8 -*-
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
OUTPUTS = [r'../data/train_media.csv', r'../data/test_media.csv']

header = ['rank', 'media_id', 'media_ft', 'label']

# create a map of media_id to media first type
media_info = {}
with open(r'../data/ccf_media_info.csv', 'r') as media:
    media.readline()
    while True:
        lines = media.readlines(10000)
        if not lines:
            break
        for line in lines:
            line = line.split(',')
            ft = ''
            if line[2] == '垂直':
                ft = '0'
            elif line[2] == '网盟':
                ft = '1'
            else:
                ft = '2'

            media_info[line[0]] = ft

    
# set media first type
for i in range(0, 2):
    saved = open(OUTPUTS[i], 'w')
    saved.write(','.join(header)+'\n') # write header

    with open(INPUTS[i], 'r') as origin:
        origin.readline() # ignore original header
        while True:
            lines = origin.readlines(10000)
            if not lines:
                break
            for line in lines:
                line = line.split(',')
                first_type = '3' if media_info.get(line[18]) is None else media_info[line[18]]
                instance = [line[0], line[18], first_type, line[21]]
                instance = ','.join(instance) # label has a '\n'
                saved.write(instance)

    saved.close()

