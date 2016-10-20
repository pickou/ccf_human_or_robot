# convert original data to csv file
# (replace '\x01' by ',')

sample_size = 1000000 # size
i=1#the i_th file
choose=0#choose train(0) or test(1)
temp=False#choose to generate a temp file to test
name_l=['AdMaster_train_dataset','test_data']
name=name_l[choose]
file_name=['train_data_csv','test_data_csv']
saved = open('./{0}/{1}_{2}.csv'.format(file_name[choose],name,i), 'w')
file_open_name=['AdMaster_train_dataset','final_ccf_test_0919']
number_lines = 0
dt='1'
lines=open(file_open_name[choose])
for line in lines:
    #line= line.replace('\n','')
    line=line.replace('\x01',',')
    line_list=line.split(',')
    temp=line_list[0:4]
    if choose==0:
        temp=temp+line_list[-1:]
    else:
        #如果是test文件则多加一列全为0的label
        temp=temp+['0\n']
    #print temp
    line=','.join(temp)
    # print line
    number_lines=number_lines+1
    if(line_list[1]==dt):#同一天的记录写到一个文件中
        saved.write(line)
    elif(line_list[1]!=dt):
        print line_list[1],dt
        dt=str(int(dt)+1)
        saved.close()
        i=i+1
        #print dt
        saved=open('./{0}/{1}_{2}.csv'.format(file_name[choose],name,i), 'w')
        saved.write(line)
saved.close()
                

                
                

