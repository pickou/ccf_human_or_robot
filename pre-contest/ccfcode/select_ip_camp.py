path = '../origin/'
name = ['AdMaster_train_dataset','final_ccf_test_0919']
choose = 0
fname=['train','test']
for choose in range(0,2):
    saved=open('../data/ip_camp_{0}.csv'.format(fname[choose]),'w')
    lines=open(path+name[choose])
    for line in lines:
        line=line.replace('\x01',',')
        line_list=line.split(',')
        #if line_list[1]!='1':
        #    break
        temp=line_list[0:2]+line_list[3:4]+line_list[10:12]
        if(choose==0):#train
            temp=temp+line_list[-1:]
        else:
            temp=temp+['0\n']
    #print temp
        line=','.join(temp)
        saved.write(line)
    saved.close()
