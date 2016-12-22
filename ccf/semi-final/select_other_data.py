attributes = [
'dt',                     # 0
'cookie',                 # 1
'f',                      # 2
'timestamps',             # 3
'camp',                   # 4
'play',                   # 5
'channel',                # 6
'creativeid',            # 7
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

INPUTS_train= [r'./data/ccf_data_{0}'.format(i) for i in range(1,4)]
INPUTS_test=[r'./data/test_data_{0}_1118'.format(i) for i in range(1,3)]
fname=['train','test']
SELECTED=[0,5,6,8,9,10,11,12,13,14,15,16,20,22]
header=[attributes[x] for x in SELECTED]
dt='160808'
for i in range(0,1):
    j=0
    flag=0
    saved=open('./data/{0}_other_{1}.csv'.format(fname[i],j),'w')

    if(i==0):
        saved.write(','.join(header)+'\n')
    else:
        saved.write('row_number,'+','.join(header)+'\n')
    if(i==0):#train
        SELECTED=[0,5,6,8,9,10,11,12,13,14,15,16,20,22] #train
        for f in INPUTS_train:
            with open(f, 'r') as origin:
                if(flag==0):
                    lines=origin.readline()
                while True:
                    lines = origin.readlines(10000)
                    if not lines:
                        break
                    for line in lines:
                        line=line.split(',')
                        if(flag==0):
                            dt=line[0]
                            flag=1
                        instance=[line[x] for x in SELECTED]
                        instance = ','.join(instance)
                        if(line[0]==dt):
                            saved.write(instance)
                        else:
                            saved.close()
                            dt=line[0]
                            j=j+1
                            saved=open('./data/{0}_other_{1}.csv'.format(fname[i],j),'w')
                            saved.write(','.join(header)+'\n')
                            saved.write(instance)
        saved.close()
    if(i==1):#test
        SELECTED=[0,1,2,3,4,5,8,22] #test 0->row_number 1->dt
        for f in INPUTS_test:
            with open(f, 'r') as origin:
                if(flag==0):
                    lines=origin.readline()
                while True:
                    lines = origin.readlines(10000)
                    if not lines:
                        break
                    for line in lines:
                        line=line.replace('\n','')
                        line=line.split(',')
                        if(flag==0):
                            dt=line[1]
                            flag=1
                        instance=[line[x] for x in SELECTED]
                        instance = ','.join(instance)+',0\n'
                        if(line[1]==dt):
                            saved.write(instance)
                        else:
                            saved.close()
                            dt=line[1]
                            j=j+1
                            saved=open('./data/{0}_other_{1}.csv'.format(fname[i],j),'w')
                            saved.write('row_number,'+','.join(header)+'\n')
                            saved.write(instance)
        saved.close()
