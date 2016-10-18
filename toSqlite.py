import sqlite3
i=0
k=0
sqlquery="INSERT INTO train"+" "+" values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
sqlquery1="INSERT INTO test"+" "+" values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
ccf_robot=sqlite3.connect('ccf_robot.db')
print "open database successfully!"
#delete table
#create train table
ccf_robot.execute('''CREATE TABLE if not exists train\
                 (rank text primary key,dt long int,cookie text,ip text,idfa text,imei text,\
                 android text,openudid text,mac text,timestamps text,cap text,\
                  creativeid text,mobile_os text,mobile_type text,app_key_md5 text,app_name_md5,\
                  placementid text,useragent text,mediaid text,os_type text,born_time text,\
                  label char);''')
#create test table
ccf_robot.execute('''CREATE TABLE if not exists test\
                 (rank text primary key,dt long int,cookie text,ip text,idfa text,imei text,\
                 android text,openudid text,mac text,timestamps text,cap text,\
                creativeid text,mobile_os text,mobile_type text,app_key_md5 text,app_name_md5,\
                  placementid text,useragent text,mediaid text,os_type text,born_time text);''')
#get train data to database
train_file=open('AdMaster_train_dataset')
for line in train_file:
    train_data=line.replace('\n','').split('\x01')
    train_data=tuple(train_data)
    ccf_robot.execute(sqlquery,train_data) 
    print k
    k=k+1
train_file.close()
'''
for i in range(0,43):
    train_data=open(r'D:\\AdMaster_competition_dataset\train_data_csv\AdMaster_train_dataset_1000000_{0}.csv'.format(i))
    for line in train_data:
        data=line.split(',')
        data=tuple(data)
        print k
        k=k+1
      #  if(k==2):break
        ccf_robot.execute(sqlquery,data)
    train_data.close()
'''
#get test data to database
test_file=open('final_ccf_test_0919')
for line in test_file:
    test_data=line.replace('\n','').split('\x01')
    test_data=tuple(test_data)
    ccf_robot.execute(sqlquery1,test_data)
    k=k+1
    print k
test_file.close()
#save changes
ccf_robot.commit()
#create test table
ccf_robot.close()
