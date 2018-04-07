# encoding=utf-8

import os
import random
import pandas as pd
from pandas import DataFrame
import time
DATA_DIR ='./data/'
TMP_DIR = DATA_DIR + 'tmp/'
print TMP_DIR
if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

TRAIN_HEADER = ['dt,cookie,f,timestamps,camp,play,channel,creativeid,idfa,mobile_mac,mobile_openudid,imei,android_id,mobile_os,mobile_type,mobile_app_key,mobile_app_name,placementid,useragent,global_mediaid,os_type,born_time,label']

TEST_HEADER = ['row_number,dt,cookie,f,timestamps,camp,play,channel,creativeid,idfa,mobile_mac,mobile_openudid,imei,android_id,mobile_os,mobile_type,mobile_app_key,mobile_app_name,placementid,useragent,global_mediaid,os_type,born_time']


###############################################################################
# sample training data into train and test
###############################################################################
def sampling():
    """sample training dataset into train and test"""
    raw = open(DATA_DIR + 'train', 'r')
    train = open(TMP_DIR + 'train', 'w')
    train.write(raw.readline()) # write header

    test = open(TMP_DIR + 'test', 'w')
    with open(DATA_DIR + 'test', 'r') as f:
        test.write(f.readline()) # write header

    test_label = open(TMP_DIR + 'test-label', 'w')
    test_label.write('label\n')
    row = 0
    for line in raw:
        i = random.randint(0, 4)
        if i == 0: # test data
            index = line.rfind(',')
            test.write(str(row) + ',' + line[:index] + '\n')
            test_label.write(line[index+1:])
            row += 1
        else:
            train.write(line)

    raw.close()
    train.close()
    test.close()
    test_label.close()


###############################################################################
# project columns from raw data
###############################################################################
def project(raw, columns):
    """project columns from raw file

    args:
      columns: the columns to project
    """

    dataset = open(raw, 'r')
    header = dataset.readline().rstrip('\n').split(',')
    selected = []
    for col in columns:
        try:
            index = header.index(col)
            selected.append(index)
        except ValueError:
            print(col + 'not in raw data!')
            dataset.close()
            return

    project = open(raw + '-' + '-'.join(columns), 'w')
    project.write(','.join(columns) + '\n')  # write header
    for data in dataset:
        temp = data.rstrip('\n').split(',')
        data = [temp[i] for i in selected]
        project.write(','.join(data) + '\n')

    dataset.close()
    project.close()


###############################################################################
# get a dict of (global_mediaid: media_first_type)
###############################################################################
def mediaid_2_media_first_type():
    """get a dict of (global_mediaid: media_first_type)"""
    mi2mft = {}
    with open(DATA_DIR + 'ccf_media_info.csv', 'r') as info:
        info.readline()  # ignore header
        FTI = 2  # IMPORTANT, first type index!
        for line in info:
            line = line.split(',')
            ft = '2'  # first type is others
            if line[FTI] == '垂直':
                ft = '0'  # first type is '垂直'
            elif line[FTI] == '网盟':
                ft = '1'  # first type is '网盟'

            mi2mft[line[0]] = ft

    return mi2mft


###############################################################################
# set media first type for log record of raw file
###############################################################################
def set_media_first_type(raw):
    """set media first type for log record of raw file"""

    mi2mft = mediaid_2_media_first_type() # a dict of media id to media first type

    dataset = open(raw, 'r')
    MII = dataset.readline().split(',').index('global_mediaid') # media id index(MII) in each record

    store = open(raw + '-media_first_type', 'w')
    store.write("media_first_type\n")

    for record in dataset:
        record = record.split(',')
        ft = mi2mft.get(record[MII], '3')
        store.write(ft + '\n')

    dataset.close()
    store.close()

###############################################################################
#ts_born
###############################################################################
def timestamps_minus_born_time(raw_file):
    dataset=open(raw_file,'r')
    header=dataset.readline().rstrip('\n').split(',')
    ts_index=header.index('timestamps')
    bt_index=header.index('born_time')

    store=open(raw_file+'-ts_bt','w')
    store.write('timestamps_minus_born_time\n')

    for record in dataset:
        attributes=record.rstrip('\n').split(',')
        timestamps=int(attributes[ts_index])
        born_time=attributes[bt_index]

        try:
            born_time_tricks=int(time.mktime(time.striptime(born_time,'%y%m%H%M%S')))
        except:
            born_time_tricks=timestamps+1
        store.write(str(timestamps-born_time_tricks)+'\n')
     dataset.close()
     store.close()


###############################################################################
# set platform for log record of raw file
###############################################################################
def set_platform(raw):
    """set platform for log record of raw file"""
    dataset = open(raw, 'r')
    header = dataset.readline().rstrip('\n').split(',')

    CONSIDER = ['idfa','mobile_mac','mobile_openudid','imei','android_id','mobile_os','mobile_type','mobile_app_key','mobile_app_name']
    selected = [header.index(x) for x in CONSIDER]

    store = open(raw + '-platform', 'w')
    store.write('platform\n')

    mobile_keywords = ['Windows%20Phone', 'Android', 'android', 'CFNetwork', 'fhone', 'BlackBerry', 'Mobile', 'Tablet', 'fod', 'fad', 'iOS']
    for record in dataset:
        platform = None  # platform is '1' for mobile and '0' for pc
        attributes = record.rstrip('\n').split(',')
        for x in selected:
            if attributes[x] != '':
                platform = '1'  # mobile
                break

        if not platform:
            for word in mobile_keywords:
                if word in record:
                    platform = '1'  # mobile
                    break

        if not platform:
            platform = '0'  # pc

        store.write(platform + '\n')

    dataset.close()
    store.close()


###############################################################################
# statistic features extraction from raw file
###############################################################################
def statistic(rawfile):
    def rawfile_type():
        i = rawfile.rfind('/')
        return rawfile[i+1:]

    if rawfile_type() == 'train':
        csvfile = rawfile + '-dt-cookie-f-placementid-label'
        if not os.path.exists(csvfile):
            project(rawfile, ['dt', 'cookie', 'f', 'placementid', 'label'])
        raw = pd.read_csv(csvfile, dtype={'dt':int, 'cookie':object, 'f':object, 'placementid':object, 'label':int})
        raw['row_number'] = pd.Series([i for i in range(raw.shape[0])], index=raw.index)
    else:
        csvfile = rawfile + '-row_number-dt-cookie-f-placementid'
        if not os.path.exists(csvfile):
            project(rawfile, ['row_number', 'dt', 'cookie', 'f', 'placementid'])
        raw = pd.read_csv(csvfile, dtype={'row_number':int, 'dt':int, 'cookie':object, 'f':object, 'placementid':object})
        raw['label'] = pd.Series([0 for i in range(raw.shape[0])], index=raw.index)

    need = raw[['row_number', 'dt', 'cookie', 'f', 'label']]

    data = raw[['f', 'dt', 'label']]
    f_dt = data.groupby(['f', 'dt']).count().reset_index(level=['f', 'dt'])
    f_dt.rename(columns={'label':'f_per_dt'}, inplace=True)
    need = pd.merge(need, f_dt,how='left', on=['f', 'dt'])
    del f_dt

    data = raw[['cookie', 'dt', 'label']]
    cookie_dt = data.groupby(['cookie', 'dt']).count().reset_index(level=['cookie', 'dt'])
    cookie_dt.rename(columns={'label':'cookie_per_dt'}, inplace=True)
    need = pd.merge(need, cookie_dt,how='left', on=['cookie', 'dt'],sort=False)
    del cookie_dt

    data = raw[['dt','camp','label']]
    camp_dt = data.groupby(['dt','camp']).count().reset_index(level=['dt','camp'])
    camp_dt.rename(columns={'label':'camp_dt'},inplace=True)
    need = pd.merge(need,camp_dt,how='left',on=['dt','camp'],sort=False)
    del camp_dt

    data = raw[['dt','f','camp','label']]
    ip_camp_dt = data.groupby(['dt','f','camp']).count().reset_index(level=['dt','f','camp'])
    ip_camp_dt.rename(columns={'label':'ip_camp_dt'},inplace=True)
    need = pd.merge(raw,ip_camp_dt,how='left',on=['dt','f','camp'],sort=False)

    data = raw[['cookie', 'f', 'label']]
    cookie_f = data.groupby(['cookie', 'f']).count().reset_index(level=['cookie', 'f'])
    cookie_f.rename(columns={'label':'cookie_per_f'}, inplace=True)
    need = pd.merge(need, cookie_f,how='left', on=['cookie', 'f'],sort=False)
    del cookie_f

    data = raw[['cookie','dt','label']]
    cookie_dt = data.groupby(['cookie','dt']).count().reset_index(level=['dt','cookie'])
    cookie_dt.rename(columns={'label':'cookie_dt'},inplace=True)
    need=pd.merge(raw,cookie_dt,how='left',on=['dt','cookie'],sort=False)
    del cookie_dt

    data = raw[['placementid', 'f']]
    del raw
    placementid_f = data.groupby(['placementid', 'f']).count().reset_index(level=['placementid', 'f'])
    placementid_f = placementid_f.groupby(['f']).count().reset_index(level=['f'])
    placementid_f.rename(columns={'placementid':'placementid_per_f'}, inplace=True)
    need = pd.merge(need, placementid_f, how='left',on=['f'],sort=False)
    del placementid_f

    need = need[['row_number', 'f_per_dt', 'cookie_per_dt', 'cookie_per_f', 'camp_dt','cookie_dt','ip_camp_dt','placementid_per_f', 'label']]
    need = need.sort_values(by='row_number')
    need = need = need[['label', 'f_per_dt', 'cookie_per_dt', 'cookie_per_f','camp_dt','cookie_dt','ip_camp_dt', 'placementid_per_f']]
    need.to_csv(rawfile + '-stat', index=False)


###############################################################################
# merge features to final csv
###############################################################################
def merge_features(raw):
    with open(raw + '-platform', 'r') as f:
        f.readline() # ignore header
        platform = f.readlines()

    with open(raw + '-media_first_type', 'r') as f:
        f.readline() # ignore header
        firsttype = f.readlines()
    with open(raw+'-time','r') as f:
        f.readline()
        ts=f.readlines()
    stat = open(raw + '-stat', 'r')
    stat.readline() # ignore header
    final = open(raw + '-final', 'w')

    with open(raw+'-camp_cookie_stat','r') as f:
        f.readline()
        camp_cookie=f.readlines()

    i = 0
    for line in stat:
        line = line.rstrip('\n')
        data = line + ',' +ts[i].rstrip('\n')+','+ camp_cookie[i].rstrip('\n')+ ',' + platform[i].rstrip('\n') + ',' + firsttype[i]
        final.write(data)
        i += 1

    stat.close()
    final.close()


###############################################################################
# main
###############################################################################
def offline():
    data = TMP_DIR + 'train'

    if not os.path.exists(data):
        sampling()

    set_media_first_type(data)
    set_platform(data)
    statistic(data)
    merge_features(data)

    data = TMP_DIR + 'test'
    set_media_first_type(data)
    set_platform(data)
    statistic(data)
    merge_features(data)


def online():
    data = DATA_DIR + 'train'
    #set_media_first_type(data)
    #set_platform(data)
    #statistic(data)
    merge_features(data)

    data = DATA_DIR + 'test'
    #set_media_first_type(data)
    #set_platform(data)
    #statistic(data)
    merge_features(data)



if __name__ == '__main__':
    #offline()
   # online()
   data=DATA_DIR+'train'
   timestamps_minus_born_time(data)
   data=DATA_DIR+'test'
   timestamps_minus_born_time(data)





