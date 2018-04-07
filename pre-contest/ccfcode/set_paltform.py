def platform(line):
    """Set platform of log

    line: str
        log string

    return: str
        '0' for PC, '1' MOBILE
    """

    PC = '0'
    MOBILE = '1'

    attr = line.split(',')
    if attr[4] != '' or attr[5] != '' or attr[6] != '' or attr[7] != '' or attr[8] != '':
        return MOBILE
    if attr[12] != '' or attr[13] != '' or attr[14] != '' or attr[15] != '':
        return MOBILE

    mobile_keywords = ['Windows%20Phone', 'Android', 'android', 'CFNetwork', 'iPhone',
                       'BlackBerry', 'Mobile', 'Tablet', 'iPod', 'iPad', 'iOS']

    for word in mobile_keywords:
        if word in line:
            return MOBILE

    return PC




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
OUTPUTS = [r'../data/train_platform.csv', r'../data/test_platform.csv']

#SELECTED = [0, 17, 21]

header = ['rank', 'platform', 'label']

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
                p = platform(line)
                line = line.split(',')
                instance = [line[0], p, line[21]]
                instance = ','.join(instance) # label has a '\n'
                saved.write(instance)

    saved.close()
